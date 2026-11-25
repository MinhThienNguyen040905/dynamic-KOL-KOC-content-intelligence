import argparse
import json
import time
from pathlib import Path

from kol.broker import Publisher
from kol.config import RAW_TOPICS
from kol.models import Event, utcnow


def read_events(path, run_id):
    with Path(path).open(encoding="utf-8") as source:
        for line_number, line in enumerate(source, 1):
            if not line.strip():
                continue
            try:
                values = json.loads(line)
                values.pop("event_id", None)
                values.update(run_id=run_id, mode="replay", ingested_at=utcnow())
                yield Event.create(**values)
            except (ValueError, TypeError, KeyError) as exc:
                raise ValueError(f"Invalid sample at line {line_number}: {exc}") from exc


def main():
    parser = argparse.ArgumentParser(description="Replay source JSONL; preserve source timestamps")
    parser.add_argument("--file", default="data/samples/demo.jsonl")
    parser.add_argument("--run-id", default="demo")
    parser.add_argument("--interval", type=float, default=0.2)
    args = parser.parse_args()
    if args.interval < 0:
        parser.error("--interval must be nonnegative")
    events = list(read_events(args.file, args.run_id))  # Validate all input before publishing.
    publisher = Publisher()
    for event in events:
        publisher.send(
            RAW_TOPICS[event.event_type], event.creator_id, event.model_dump(mode="json")
        )
        publisher.flush()
        time.sleep(args.interval)
    print(f"Published {len(events)} events; run_id={args.run_id}; mode=replay", flush=True)


if __name__ == "__main__":
    main()
