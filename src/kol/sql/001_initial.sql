CREATE TABLE IF NOT EXISTS schema_migrations (
    version text PRIMARY KEY,
    applied_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS events (
    run_id text NOT NULL,
    event_id text NOT NULL,
    event_type text NOT NULL,
    source text NOT NULL,
    source_id text NOT NULL,
    creator_id text NOT NULL,
    event_time timestamptz NOT NULL,
    observed_at timestamptz NOT NULL,
    ingested_at timestamptz NOT NULL,
    mode text NOT NULL,
    body jsonb NOT NULL,
    stored_at timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (run_id, event_id)
);
CREATE INDEX IF NOT EXISTS events_creator_time ON events (run_id, creator_id, event_time);

CREATE TABLE IF NOT EXISTS current_events (
    run_id text NOT NULL,
    source text NOT NULL,
    event_type text NOT NULL,
    source_id text NOT NULL,
    event_id text NOT NULL,
    event_time timestamptz NOT NULL,
    observed_at timestamptz NOT NULL,
    PRIMARY KEY (run_id, source, event_type, source_id),
    FOREIGN KEY (run_id, event_id) REFERENCES events (run_id, event_id)
);

CREATE TABLE IF NOT EXISTS analyses (
    run_id text NOT NULL,
    event_id text NOT NULL,
    model_version text NOT NULL,
    body jsonb NOT NULL,
    available_at timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (run_id, event_id, model_version),
    FOREIGN KEY (run_id, event_id) REFERENCES events (run_id, event_id)
);

INSERT INTO schema_migrations(version) VALUES ('001') ON CONFLICT DO NOTHING;

