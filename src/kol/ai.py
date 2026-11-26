"""Deterministic integration baseline, not the final research model."""

import re

from fastapi import FastAPI

from kol.models import Analysis, Event, Evidence, Opinion

app = FastAPI(title="KOL AI — rules baseline", version="0.1.0")
BRANDS = ("Samsung", "Apple", "Xiaomi", "Sony", "iPhone")
TOPIC_TERMS = {
    "technology": ("máy", "pin", "điện thoại", "iphone", "camera"),
    "beauty": ("son", "kem", "skincare", "da mặt"),
}
RULES = (
    ("pin yếu", "battery", "negative", "product"),
    ("pin tốt", "battery", "positive", "product"),
    ("giá cao", "price", "negative", "product"),
    ("giá hợp lý", "price", "positive", "product"),
    ("review dễ hiểu", "presentation", "positive", "creator"),
    ("review khó hiểu", "presentation", "negative", "creator"),
)


def matches(text, phrase):
    # re.finditer preserves offsets in the original Unicode source text.
    return re.finditer(r"(?<!\w)" + re.escape(phrase) + r"(?!\w)", text, re.IGNORECASE)


def analyze(event: Event) -> Analysis:
    brands, opinions, topics = [], [], []
    fields = ("title", "description") if event.event_type == "content" else ("text",)
    for field in fields:
        text = event.payload.get(field, "")
        for brand in BRANDS:
            for match in matches(text, brand):
                brands.append(
                    Evidence(field=field, start=match.start(), end=match.end(), text=match.group())
                )
        if event.event_type == "comment":
            for phrase, aspect, sentiment, entity_type in RULES:
                for match in matches(text, phrase):
                    opinions.append(
                        Opinion(
                            entity_text="implicit",
                            entity_type=entity_type,
                            aspect=aspect,
                            sentiment=sentiment,
                            evidence=Evidence(
                                field=field,
                                start=match.start(),
                                end=match.end(),
                                text=match.group(),
                            ),
                        )
                    )
    if event.event_type == "content":
        text = " ".join(event.payload.get(field, "") for field in fields).lower()
        topics = [topic for topic, terms in TOPIC_TERMS.items() if any(t in text for t in terms)]
    return Analysis(
        event=event,
        model_version="rules-v1",
        topics=topics,
        brands=brands,
        opinions=opinions,
        status="no_opinion" if event.event_type == "comment" and not opinions else "success",
    )


@app.get("/health")
def health():
    return {"status": "ok", "model_version": "rules-v1", "baseline": True}


@app.post("/analyze", response_model=Analysis)
def inference(event: Event):
    return analyze(event)
