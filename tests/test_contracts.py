import json
from datetime import datetime, timezone
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from kol.ai import analyze, app
from kol.models import Analysis, Event
from kol.profiles import summarize
from kol.replay import read_events


@pytest.fixture
def events():
    return list(read_events(Path(__file__).parents[1] / "data/samples/demo.jsonl", "test"))


def test_retry_and_run_do_not_change_source_identity(events):
    event = events[1]
    data = event.model_dump(exclude={"event_id"})
    data.update(run_id="another-run", ingested_at=datetime(2026, 12, 1, tzinfo=timezone.utc))
    assert Event.create(**data).event_id == event.event_id
    data["payload"]["text"] += " Updated"
    assert Event.create(**data).event_id != event.event_id


def test_tampered_input_and_naive_time_are_rejected(events):
    data = events[1].model_dump(mode="json")
    data["payload"]["text"] = "tampered"
    with pytest.raises(ValidationError, match="event_id"):
        Event.model_validate(data)
    data = events[1].model_dump(exclude={"event_id"})
    data["event_time"] = datetime(2026, 11, 25)
    with pytest.raises(ValueError, match="timezone"):
        Event.create(**data)


def test_snapshot_identity_includes_observation_time(events):
    data = events[-1].model_dump(exclude={"event_id"})
    data["observed_at"] = datetime(2026, 11, 25, 5, tzinfo=timezone.utc)
    assert Event.create(**data).event_id != events[-1].event_id


def test_mixed_sentiment_keeps_separate_opinions_and_source_spans(events):
    result = analyze(events[1])
    assert {(o.entity_type, o.aspect, o.sentiment) for o in result.opinions} == {
        ("creator", "presentation", "positive"),
        ("product", "battery", "negative"),
    }
    for opinion in result.opinions:
        span = opinion.evidence
        assert events[1].payload["text"][span.start : span.end] == span.text
    assert analyze(events[3]).status == "no_opinion"


def test_fabricated_evidence_is_rejected(events):
    data = analyze(events[1]).model_dump(mode="json")
    data["opinions"][0]["evidence"]["text"] = "fabricated"
    with pytest.raises(ValidationError, match="Evidence"):
        Analysis.model_validate(data)


def test_profile_separates_pending_and_tuple_denominator(events):
    rows = [
        {
            "event": e.model_dump(mode="json"),
            "analysis": analyze(e).model_dump(mode="json") if i == 1 else None,
        }
        for i, e in enumerate(events[:4])
    ]
    result = summarize(rows)
    assert result["counts"]["pending"] == 3
    assert result["counts"]["analyzed_comments"] == 1
    assert result["sentiment_tuples"] == {"positive": 1, "negative": 1}
    assert result["counts"]["comments_with_opinion"] == 1


def test_ai_http_contract(events):
    client = TestClient(app)
    response = client.post("/analyze", json=events[1].model_dump(mode="json"))
    assert response.status_code == 200
    assert len(Analysis.model_validate(response.json()).opinions) == 2
    assert client.post("/analyze", json={}).status_code == 422


def test_samples_are_valid_jsonl(events):
    assert len(events) == 6
    assert len({e.event_id for e in events}) == 6
    for event in events:
        assert Event.model_validate(json.loads(event.model_dump_json())) == event
