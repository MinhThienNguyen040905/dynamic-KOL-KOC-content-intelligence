import hashlib
import json
from datetime import datetime, timezone
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Content(BaseModel):
    model_config = ConfigDict(extra="forbid")
    title: str = Field(min_length=1)
    description: str = ""
    url: str = ""


class Comment(BaseModel):
    model_config = ConfigDict(extra="forbid")
    video_id: str = Field(min_length=1)
    text: str = Field(min_length=1)
    parent_id: str | None = None
    url: str = ""


class Engagement(BaseModel):
    model_config = ConfigDict(extra="forbid")
    video_id: str = Field(min_length=1)
    view_count: int | None = Field(default=None, ge=0)
    like_count: int | None = Field(default=None, ge=0)
    comment_count: int | None = Field(default=None, ge=0)


class Event(BaseModel):
    model_config = ConfigDict(extra="forbid")
    schema_version: Literal["1"] = "1"
    event_id: str = Field(min_length=1)
    event_type: Literal["content", "comment", "engagement"]
    source: Literal["youtube", "synthetic"]
    source_id: str = Field(min_length=1)
    creator_id: str = Field(min_length=1)
    event_time: datetime
    observed_at: datetime
    ingested_at: datetime = Field(default_factory=utcnow)
    run_id: str = Field(min_length=1, max_length=100)
    mode: Literal["live", "replay"]
    payload: dict

    @field_validator("event_time", "observed_at", "ingested_at")
    @classmethod
    def aware_time(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("Timestamp must include a timezone")
        return value.astimezone(timezone.utc)

    @model_validator(mode="after")
    def validate_payload(self):
        schema = {"content": Content, "comment": Comment, "engagement": Engagement}
        self.payload = schema[self.event_type].model_validate(self.payload).model_dump()
        if self.event_id != self.fingerprint():
            raise ValueError("event_id does not match the immutable source event")
        return self

    def fingerprint(self) -> str:
        fields = self.model_dump(
            mode="json",
            include={
                "schema_version",
                "event_type",
                "source",
                "source_id",
                "creator_id",
                "event_time",
                "payload",
            },
        )
        # Snapshot identity includes its observation time, unlike a content/comment retry.
        if self.event_type == "engagement":
            fields["observed_at"] = self.observed_at.isoformat()
        return hashlib.sha256(
            json.dumps(fields, sort_keys=True, ensure_ascii=False).encode("utf-8")
        ).hexdigest()

    @classmethod
    def create(cls, **values):
        schema = {"content": Content, "comment": Comment, "engagement": Engagement}
        values["payload"] = (
            schema[values["event_type"]].model_validate(values["payload"]).model_dump()
        )
        for name in ("event_time", "observed_at", "ingested_at"):
            if name in values:
                value = values[name]
                if isinstance(value, str):
                    value = datetime.fromisoformat(value.replace("Z", "+00:00"))
                values[name] = cls.aware_time(value)
        values.setdefault("schema_version", "1")
        candidate = cls.model_construct(**values)
        values["event_id"] = candidate.fingerprint()
        return cls.model_validate(values)


class Evidence(BaseModel):
    model_config = ConfigDict(extra="forbid")
    field: Literal["title", "description", "text"]
    start: int = Field(ge=0)
    end: int = Field(gt=0)
    text: str = Field(min_length=1)


class Opinion(BaseModel):
    model_config = ConfigDict(extra="forbid")
    entity_text: str
    entity_type: Literal["creator", "product", "brand", "unknown"]
    aspect: str
    sentiment: Literal["positive", "negative", "neutral"]
    evidence: Evidence


class Analysis(BaseModel):
    model_config = ConfigDict(extra="forbid")
    event: Event
    model_version: str
    taxonomy_version: str = "pilot-v1"
    status: Literal["success", "no_opinion"]
    topics: list[str] = Field(default_factory=list)
    brands: list[Evidence] = Field(default_factory=list)
    opinions: list[Opinion] = Field(default_factory=list)
    processed_at: datetime = Field(default_factory=utcnow)

    @model_validator(mode="after")
    def valid_evidence(self):
        for span in [*self.brands, *(opinion.evidence for opinion in self.opinions)]:
            text = self.event.payload.get(span.field, "")
            if text[span.start : span.end] != span.text:
                raise ValueError("Evidence must match the original source text")
        if self.status == "no_opinion" and self.opinions:
            raise ValueError("no_opinion cannot contain opinions")
        return self
