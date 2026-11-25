import logging
import time

import httpx
from confluent_kafka import Consumer
from pydantic import ValidationError

from kol.broker import Publisher
from kol.config import settings
from kol.models import Analysis, Event

log = logging.getLogger(__name__)


def infer(client, event):
    for attempt in range(3):
        try:
            response = client.post("/analyze", json=event.model_dump(mode="json"))
            response.raise_for_status()
            result = Analysis.model_validate(response.json())
            if result.event != event or result.model_version != settings.model_version:
                raise ValueError("Inference response does not match request/model version")
            return result
        except (httpx.HTTPError, ValidationError, ValueError):
            if attempt == 2:
                raise
            time.sleep(2**attempt)


def main():
    logging.basicConfig(level=logging.INFO)
    consumer = Consumer(
        {
            "bootstrap.servers": settings.kafka_servers,
            "group.id": "ai-worker-v1",
            "auto.offset.reset": "earliest",
            "enable.auto.commit": False,
            "max.poll.interval.ms": 300000,
        }
    )
    consumer.subscribe(["ai.requests"])
    publisher = Publisher()
    try:
        with httpx.Client(base_url=settings.ai_url, timeout=30) as client:
            while True:
                message = consumer.poll(1)
                if message is None:
                    continue
                if message.error():
                    raise RuntimeError(message.error())
                try:
                    event = Event.model_validate_json(message.value())
                    result = infer(client, event)
                except (httpx.HTTPError, ValidationError, ValueError) as exc:
                    log.warning(
                        "Inference failed at offset %s: %s", message.offset(), type(exc).__name__
                    )
                    publisher.send(
                        "pipeline.dlq",
                        str(message.offset()),
                        {
                            "stage": "inference",
                            "error_type": type(exc).__name__,
                            "input": message.value().decode("utf-8", errors="replace"),
                            "topic": message.topic(),
                            "partition": message.partition(),
                            "offset": message.offset(),
                        },
                    )
                else:
                    publisher.send("ai.results", event.creator_id, result.model_dump(mode="json"))
                    log.info("Analyzed run=%s event=%s", event.run_id, event.event_id[:12])
                # A delivery error aborts the process; the uncommitted message is retried.
                publisher.flush()
                consumer.commit(message=message, asynchronous=False)
    finally:
        consumer.close()


if __name__ == "__main__":
    main()
