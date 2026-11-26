"""Opt-in tests against the local PostgreSQL service; each test isolates its run ID."""

import os
import uuid
from datetime import datetime, timezone
from pathlib import Path

import pytest

from kol.ai import analyze
from kol.db import connect, profile_rows, store_analysis, store_event
from kol.models import Event
from kol.profiles import summarize
from kol.replay import read_events

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_DB_TESTS") != "1", reason="Set RUN_DB_TESTS=1 with local PostgreSQL running"
)


@pytest.fixture
def isolated():
    run_id = f"db-test-{uuid.uuid4().hex}"
    events = list(read_events(Path(__file__).parents[1] / "data/samples/demo.jsonl", run_id))
    try:
        with connect() as conn:
            yield conn, events
    finally:
        with connect() as conn:
            for table in ("analyses", "current_events", "events"):
                conn.execute(f"DELETE FROM {table} WHERE run_id=%s", (run_id,))


def test_duplicate_result_is_not_counted_twice(isolated):
    conn, events = isolated
    result = analyze(events[1])
    store_analysis(conn, result)
    store_analysis(conn, result)
    profile = summarize(profile_rows(conn, events[1].run_id))
    assert profile["counts"]["comment"] == 1
    assert profile["sentiment_tuples"] == {"positive": 1, "negative": 1}


def test_revision_replaces_old_analysis_and_late_old_result_cannot_revert_it(isolated):
    conn, events = isolated
    old = events[1]
    store_analysis(conn, analyze(old))
    values = old.model_dump(exclude={"event_id"})
    values.update(event_time=datetime(2026, 11, 26, tzinfo=timezone.utc))
    values["payload"]["text"] = "máy X pin tốt"
    new = Event.create(**values)
    store_event(conn, new)
    pending = summarize(profile_rows(conn, old.run_id))
    assert pending["counts"]["pending"] == 1
    assert pending["sentiment_tuples"] == {}
    store_analysis(conn, analyze(new))
    store_analysis(conn, analyze(old))
    current = summarize(profile_rows(conn, old.run_id))
    assert current["counts"]["comment"] == 1
    assert current["sentiment_tuples"] == {"positive": 1}
    assert current["evidence"][0]["event_id"] == new.event_id


def test_snapshot_history_retained_while_current_pointer_is_latest(isolated):
    conn, events = isolated
    for event in (events[-1], events[-2], events[-1]):
        store_event(conn, event)
    current = profile_rows(conn, events[0].run_id)
    assert len(current) == 1
    assert current[0]["event"]["payload"]["view_count"] == 160
    count = conn.execute("SELECT count(*) AS n FROM events WHERE run_id=%s", (events[0].run_id,))
    assert count.fetchone()["n"] == 2
