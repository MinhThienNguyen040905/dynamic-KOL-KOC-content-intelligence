"""Run after `docker compose up -d --build`; validates the actual container pipeline."""

import json
import subprocess
import time
import uuid
from urllib.request import urlopen


def get(path):
    with urlopen(f"http://localhost:8000{path}", timeout=10) as response:
        return json.load(response)


def replay(run_id):
    subprocess.run(
        [
            "docker",
            "compose",
            "run",
            "--rm",
            "--no-deps",
            "replay",
            "python",
            "-m",
            "kol.replay",
            "--file",
            "data/samples/demo.jsonl",
            "--run-id",
            run_id,
            "--interval",
            "0",
        ],
        check=True,
    )


def wait_profile(run_id):
    deadline = time.monotonic() + 180
    while time.monotonic() < deadline:
        profile = get(f"/profiles/creator-tech-demo?run_id={run_id}")
        if profile["counts"]["analyzed"] == 4 and profile["counts"]["engagement"] == 1:
            return profile
        time.sleep(2)
    raise AssertionError("Pipeline did not complete within 180 seconds")


def main():
    run_id = f"smoke-{uuid.uuid4().hex[:12]}"
    replay(run_id)
    before = wait_profile(run_id)
    assert before["counts"]["content"] == 1
    assert before["counts"]["comment"] == 3
    assert before["counts"]["pending"] == 0
    assert before["sentiment_tuples"] == {"positive": 3, "negative": 1}
    replay(run_id)
    # Wait for the duplicate batch to cross both streaming queries.
    time.sleep(15)
    after = wait_profile(run_id)
    for key in ("counts", "topics", "brands", "sentiment_tuples", "aspect_sentiments"):
        assert before[key] == after[key], f"Duplicate replay changed {key}"
    snapshots = get(f"/engagement/video-001?run_id={run_id}")
    assert len(snapshots["snapshots"]) == 2
    assert snapshots["deltas"][0]["delta"]["view_count"] == 60
    assert len(after["evidence"]) == 4
    print(f"PASS: end-to-end, duplicate replay, evidence and snapshot delta; run_id={run_id}")


if __name__ == "__main__":
    main()
