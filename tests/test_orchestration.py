import copy
import json
from pathlib import Path

import pytest

from kol import orchestration

SAMPLE = Path(__file__).parents[1] / "data/samples/demo.jsonl"


def test_manifest_is_stable_on_task_retry_and_separates_dag_runs():
    first = orchestration.validate_sample(SAMPLE, "manual__first")
    assert first == orchestration.validate_sample(SAMPLE, "manual__first")
    assert first["run_id"] != orchestration.validate_sample(SAMPLE, "manual__second")["run_id"]
    assert first["events"] == 6
    assert first["expected_analyses"] == 4


def test_publication_rejects_modified_input_before_sending(tmp_path, monkeypatch):
    sample = tmp_path / "sample.jsonl"
    sample.write_bytes(SAMPLE.read_bytes())
    manifest = orchestration.validate_sample(sample, "manual__changed")
    sample.write_text("", encoding="utf-8")

    def forbidden():
        pytest.fail("A changed input must not create a producer")

    monkeypatch.setattr(orchestration, "Publisher", forbidden)
    with pytest.raises(ValueError, match="changed after validation"):
        orchestration.publish_sample(manifest)


def test_completion_requires_analysis_and_all_raw_snapshots(monkeypatch):
    manifest = orchestration.validate_sample(SAMPLE, "manual__completion")
    counts = {"content": 1, "comment": 3, "analyzed": 4, "pending": 0}
    stored = 5

    def fake_api(path):
        if path == "/runs":
            return [{"run_id": manifest["run_id"], "stored_events": stored}]
        return {"counts": counts}

    monkeypatch.setattr(orchestration, "api_get", fake_api)
    assert not orchestration.pipeline_complete(manifest)
    stored = 6
    assert orchestration.pipeline_complete(manifest)
    counts["pending"] = 1
    assert not orchestration.pipeline_complete(manifest)


def test_sample_revision_is_rejected_but_identical_retry_is_allowed(tmp_path):
    samples = [
        json.loads(line) for line in SAMPLE.read_text(encoding="utf-8").splitlines() if line.strip()
    ]
    retry = copy.deepcopy(samples[1])
    path = tmp_path / "retries.jsonl"
    path.write_text("\n".join(json.dumps(item) for item in [*samples, retry]), encoding="utf-8")
    assert orchestration.validate_sample(path, "retry")["events"] == 6
    retry["payload"]["text"] = "a new revision"
    path.write_text("\n".join(json.dumps(item) for item in [*samples, retry]), encoding="utf-8")
    with pytest.raises(ValueError, match="one content/comment revision"):
        orchestration.validate_sample(path, "revised")
