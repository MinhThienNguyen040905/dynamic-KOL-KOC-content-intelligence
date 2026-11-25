import json

from confluent_kafka import Producer

from kol.config import settings


def producer():
    return Producer(
        {
            "bootstrap.servers": settings.kafka_servers,
            "enable.idempotence": True,
            "delivery.timeout.ms": 30000,
        }
    )


class Publisher:
    """Fail the batch before advancing its offset if any delivery fails."""

    def __init__(self):
        self.client = producer()
        self.errors = []

    def send(self, topic, key, body):
        def delivered(error, _message):
            if error:
                self.errors.append(str(error))

        self.client.produce(
            topic,
            key=key.encode(),
            value=json.dumps(body, ensure_ascii=False).encode(),
            on_delivery=delivered,
        )
        self.client.poll(0)

    def flush(self):
        pending = self.client.flush(35)
        if pending or self.errors:
            raise RuntimeError(f"Kafka delivery failed: pending={pending}, errors={self.errors}")
