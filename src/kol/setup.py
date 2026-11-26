from confluent_kafka.admin import AdminClient, NewTopic

from kol.config import TOPICS, settings
from kol.db import migrate


def main():
    migrate()
    admin = AdminClient({"bootstrap.servers": settings.kafka_servers})
    existing = admin.list_topics(timeout=15).topics
    missing = [
        NewTopic(topic, num_partitions=2, replication_factor=1)
        for topic in TOPICS
        if topic not in existing
    ]
    futures = admin.create_topics(missing) if missing else {}
    for topic, future in futures.items():
        future.result()
        print(f"Created topic {topic}", flush=True)
    print("Database and topics ready", flush=True)


if __name__ == "__main__":
    main()
