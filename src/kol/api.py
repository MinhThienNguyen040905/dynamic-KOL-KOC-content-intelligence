from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse

from kol.config import settings
from kol.db import connect, profile_rows
from kol.profiles import summarize

app = FastAPI(title="Dynamic KOL/KOC Content Intelligence", version="0.1.0")


@app.get("/", include_in_schema=False)
def dashboard():
    return FileResponse(Path(__file__).parent / "static" / "index.html")


@app.get("/health")
def health():
    with connect() as conn:
        conn.execute("SELECT 1 FROM schema_migrations LIMIT 1")
    return {"status": "ok", "model_version": settings.model_version}


@app.get("/runs")
def runs():
    with connect() as conn:
        return conn.execute(
            """SELECT run_id, mode, count(*) AS stored_events, max(stored_at) AS updated_at
            FROM events GROUP BY run_id,mode ORDER BY updated_at DESC"""
        ).fetchall()


@app.get("/creators")
def creators(run_id: str = Query(default="demo", min_length=1, max_length=100)):
    with connect() as conn:
        return conn.execute(
            """SELECT e.creator_id, count(*) AS current_records
            FROM current_events c JOIN events e USING(run_id,event_id)
            WHERE e.run_id=%s GROUP BY e.creator_id ORDER BY e.creator_id""",
            (run_id,),
        ).fetchall()


@app.get("/profiles/{creator_id}")
def profile(
    creator_id: str,
    run_id: str = "demo",
    since: datetime | None = None,
    until: datetime | None = None,
):
    if any(value is not None and value.tzinfo is None for value in (since, until)):
        raise HTTPException(422, "Time filters must include a timezone")
    if since and until and since >= until:
        raise HTTPException(422, "since must be earlier than until")
    with connect() as conn:
        rows = profile_rows(conn, run_id, creator_id, since, until)
    return {
        "creator_id": creator_id,
        "run_id": run_id,
        "since": since,
        "until": until,
        "model_version": settings.model_version,
        "baseline": True,
        **summarize(rows),
    }


@app.get("/events/{event_id}")
def event(event_id: str, run_id: str = "demo"):
    with connect() as conn:
        row = conn.execute(
            "SELECT body FROM events WHERE run_id=%s AND event_id=%s", (run_id, event_id)
        ).fetchone()
    if not row:
        raise HTTPException(404, "Event not found")
    return row["body"]


@app.get("/engagement/{video_id}")
def engagement(video_id: str, run_id: str = "demo"):
    with connect() as conn:
        rows = conn.execute(
            """SELECT body FROM events WHERE run_id=%s AND source_id=%s
            AND event_type='engagement' ORDER BY observed_at,event_id""",
            (run_id, video_id),
        ).fetchall()
    snapshots = [row["body"] for row in rows]
    deltas = []
    for previous, current in zip(snapshots, snapshots[1:]):
        delta = {}
        for field in ("view_count", "like_count", "comment_count"):
            a, b = previous["payload"].get(field), current["payload"].get(field)
            delta[field] = None if a is None or b is None else b - a
        deltas.append(
            {
                "from": previous["observed_at"],
                "until": current["observed_at"],
                "delta": delta,
                "has_decrease": any(value is not None and value < 0 for value in delta.values()),
            }
        )
    return {"run_id": run_id, "video_id": video_id, "snapshots": snapshots, "deltas": deltas}
