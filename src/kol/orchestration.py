"""Reusable finite workflow steps. Airflow-specific imports live only in the DAG file."""

import hashlib
import json
import os
from pathlib import Path
from urllib.parse import quote, urlencode
from urllib.request import urlopen

from kol.broker import Publisher
from kol.config import RAW_TOPICS
from kol.replay import read_events


def api_get(path):
    base = os.getenv("PROJECT_API_URL", "http://localhost:8000").rstrip("/")
    with urlopen(f"{base}{path}", timeout=10) as response:
        return json.load(response)


def project_run_id(airflow_run_id):
    return "airflow-" + hashlib.sha256(airflow_run_id.encode()).hexdigest()[:24]


def validate_sample(path, airflow_run_id):
    path = str(Path(path).resolve())
    data = Path(path).read_bytes()
    run_id = project_run_id(airflow_run_id)
    events = list(read_events(path, run_id))
    if not events:
        raise ValueError("Replay input must not be empty")
    # Avoid ambiguous manifest counts when the input contains retries or source revisions.
    keys = {
        (event.source, event.event_type, event.source_id)
        for event in events
        if event.event_type != "engagement"
    }
    unique_ai = {
        (event.source, event.event_type, event.source_id, event.event_id)
        for event in events
        if event.event_type != "engagement"
    }
    if len(keys) != len(unique_ai):
        raise ValueError("Use one content/comment revision per source in a replay workflow")
    return {
        "path": path,
        "sha256": hashlib.sha256(data).hexdigest(),
        "run_id": run_id,
        "events": len({event.event_id for event in events}),
        "expected_analyses": len(unique_ai),
        "creators": sorted({event.creator_id for event in events}),
    }


def publish_sample(manifest):
    if hashlib.sha256(Path(manifest["path"]).read_bytes()).hexdigest() != manifest["sha256"]:
        raise ValueError("Sample changed after validation; start a new workflow run")
    publisher = Publisher()
    for event in read_events(manifest["path"], manifest["run_id"]):
        publisher.send(
            RAW_TOPICS[event.event_type], event.creator_id, event.model_dump(mode="json")
        )
        publisher.flush()
    return manifest


def completion_summary(manifest):
    counts = {"content": 0, "comment": 0, "analyzed": 0, "pending": 0}
    for creator in manifest["creators"]:
        profile = api_get(
            f"/profiles/{quote(creator, safe='')}?{urlencode({'run_id': manifest['run_id']})}"
        )
        for key in counts:
            counts[key] += profile["counts"][key]
    runs = api_get("/runs")
    stored = sum(run["stored_events"] for run in runs if run["run_id"] == manifest["run_id"])
    return {
        "run_id": manifest["run_id"],
        "stored_events": stored,
        **counts,
        "complete": stored == manifest["events"]
        and counts["analyzed"] == manifest["expected_analyses"]
        and counts["pending"] == 0,
    }


def pipeline_complete(manifest):
    return completion_summary(manifest)["complete"]
