import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    database_url: str = os.getenv(
        "DATABASE_URL", "postgresql://kol:kol_local_dev@localhost:5432/kol_intelligence"
    )
    kafka_servers: str = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    ai_url: str = os.getenv("AI_SERVICE_URL", "http://localhost:8001")
    model_version: str = os.getenv("MODEL_VERSION", "rules-v1")


settings = Settings()
RAW_TOPICS = {"content": "content.raw", "comment": "comments.raw", "engagement": "engagement.raw"}
TOPICS = [*RAW_TOPICS.values(), "ai.requests", "ai.results", "pipeline.dlq"]
