from pathlib import Path

import psycopg
from psycopg.rows import dict_row
from psycopg.types.json import Jsonb

from kol.config import settings
from kol.models import Analysis, Event


def connect():
    return psycopg.connect(settings.database_url, row_factory=dict_row, connect_timeout=10)


def migrate():
    with connect() as conn:
        # All schema changes must be added as new numbered files; keep applied files immutable.
        conn.execute("SELECT pg_advisory_xact_lock(363001)")
        conn.execute("""CREATE TABLE IF NOT EXISTS schema_migrations (
            version text PRIMARY KEY, applied_at timestamptz NOT NULL DEFAULT now())""")
        for path in sorted((Path(__file__).parent / "sql").glob("*.sql")):
            version = path.stem.split("_")[0]
            if not conn.execute(
                "SELECT 1 FROM schema_migrations WHERE version=%s", (version,)
            ).fetchone():
                conn.execute(path.read_text(encoding="utf-8"))


def store_event(conn, event: Event):
    values = event.model_dump()
    conn.execute(
        """INSERT INTO events
        (run_id,event_id,event_type,source,source_id,creator_id,event_time,
         observed_at,ingested_at,mode,body)
        VALUES (%(run_id)s,%(event_id)s,%(event_type)s,%(source)s,%(source_id)s,
         %(creator_id)s,%(event_time)s,%(observed_at)s,%(ingested_at)s,%(mode)s,%(body)s)
        ON CONFLICT (run_id,event_id) DO NOTHING""",
        {**values, "body": Jsonb(event.model_dump(mode="json"))},
    )
    conn.execute(
        """INSERT INTO current_events
        (run_id,source,event_type,source_id,event_id,event_time,observed_at)
        VALUES (%(run_id)s,%(source)s,%(event_type)s,%(source_id)s,
          %(event_id)s,%(event_time)s,%(observed_at)s)
        ON CONFLICT (run_id,source,event_type,source_id) DO UPDATE SET
          event_id=EXCLUDED.event_id, event_time=EXCLUDED.event_time,
          observed_at=EXCLUDED.observed_at
        WHERE (EXCLUDED.event_time,EXCLUDED.observed_at,EXCLUDED.event_id) >
          (current_events.event_time,current_events.observed_at,current_events.event_id)""",
        values,
    )


def store_analysis(conn, result: Analysis):
    store_event(conn, result.event)
    conn.execute(
        """INSERT INTO analyses(run_id,event_id,model_version,body) VALUES (%s,%s,%s,%s)
        ON CONFLICT (run_id,event_id,model_version) DO NOTHING""",
        (
            result.event.run_id,
            result.event.event_id,
            result.model_version,
            Jsonb(result.model_dump(mode="json")),
        ),
    )


def profile_rows(conn, run_id, creator_id=None, since=None, until=None):
    return conn.execute(
        """SELECT e.body AS event, a.body AS analysis, a.available_at
        FROM current_events c JOIN events e USING (run_id,event_id)
        LEFT JOIN analyses a ON a.run_id=e.run_id AND a.event_id=e.event_id
          AND a.model_version=%s
        WHERE e.run_id=%s AND (%s::text IS NULL OR e.creator_id=%s)
          AND (%s::timestamptz IS NULL OR e.event_time >= %s)
          AND (%s::timestamptz IS NULL OR e.event_time < %s)
        ORDER BY e.event_time, e.event_id""",
        (settings.model_version, run_id, creator_id, creator_id, since, since, until, until),
    ).fetchall()
