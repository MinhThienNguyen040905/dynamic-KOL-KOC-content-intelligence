"""Two Structured Streaming queries with durable checkpoints and idempotent DB sinks."""

from pydantic import ValidationError

from kol.broker import Publisher
from kol.config import RAW_TOPICS, settings
from kol.db import connect, store_analysis, store_event
from kol.models import Analysis, Event


def normalize_partition(rows):
    publisher = Publisher()
    with connect() as conn:
        for row in rows:
            try:
                event = Event.model_validate_json(row.raw)
                if RAW_TOPICS[event.event_type] != row.topic:
                    raise ValueError("Source topic does not match event type")
            except (ValidationError, ValueError) as exc:
                publisher.send(
                    "pipeline.dlq",
                    f"{row.topic}:{row.partition}:{row.offset}",
                    {
                        "stage": "normalize",
                        "error_type": type(exc).__name__,
                        "input": row.raw,
                        "topic": row.topic,
                        "partition": row.partition,
                        "offset": row.offset,
                    },
                )
                continue
            with conn.transaction():
                store_event(conn, event)
            if event.event_type != "engagement":
                publisher.send("ai.requests", event.creator_id, event.model_dump(mode="json"))
            # Bound producer memory and preserve ordering around the per-event DB commit.
            publisher.flush()
        publisher.flush()


def results_partition(rows):
    publisher = Publisher()
    with connect() as conn:
        for row in rows:
            try:
                result = Analysis.model_validate_json(row.raw)
            except ValidationError as exc:
                publisher.send(
                    "pipeline.dlq",
                    f"{row.partition}:{row.offset}",
                    {
                        "stage": "results",
                        "error_type": type(exc).__name__,
                        "input": row.raw,
                        "topic": row.topic,
                        "partition": row.partition,
                        "offset": row.offset,
                    },
                )
            else:
                with conn.transaction():
                    store_analysis(conn, result)
        publisher.flush()


def normalize_batch(batch, batch_id):
    batch.persist()
    try:
        # Deterministic batch path makes a Spark batch retry replace its own archive.
        batch.write.mode("overwrite").parquet(f"/data/archive/raw/batch-{batch_id}")
        batch.foreachPartition(normalize_partition)
    finally:
        batch.unpersist()


def results_batch(batch, batch_id):
    batch.foreachPartition(results_partition)


def main():
    from pyspark.sql import SparkSession

    spark = SparkSession.builder.appName("kol-content-intelligence").getOrCreate()
    spark.sparkContext.setLogLevel("WARN")
    spark.conf.set("spark.sql.shuffle.partitions", "2")

    def source(topics):
        return (
            spark.readStream.format("kafka")
            .option("kafka.bootstrap.servers", settings.kafka_servers)
            .option("subscribe", topics)
            .option("startingOffsets", "earliest")
            .option("maxOffsetsPerTrigger", 200)
            .load()
            .selectExpr("CAST(value AS STRING) AS raw", "topic", "partition", "offset")
        )

    (
        source(",".join(RAW_TOPICS.values()))
        .writeStream.foreachBatch(normalize_batch)
        .option("checkpointLocation", "/data/checkpoints/normalize-v1")
        .trigger(processingTime="5 seconds")
        .start()
    )
    (
        source("ai.results")
        .writeStream.foreachBatch(results_batch)
        .option("checkpointLocation", "/data/checkpoints/results-v1")
        .trigger(processingTime="5 seconds")
        .start()
    )
    spark.streams.awaitAnyTermination()


if __name__ == "__main__":
    main()
