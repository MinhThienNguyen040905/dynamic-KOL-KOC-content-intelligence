"""Orchestrate a bounded replay; Kafka, Spark and inference workers remain long-running."""

from datetime import datetime, timedelta, timezone

from airflow.providers.standard.sensors.python import PythonSensor
from airflow.sdk import DAG, get_current_context, task
from kol.orchestration import (
    api_get,
    completion_summary,
    pipeline_complete,
    publish_sample,
    validate_sample,
)

with DAG(
    dag_id="kol_replay_pipeline",
    description="Validate synthetic data, publish to Kafka, verify end-to-end completion",
    start_date=datetime(2026, 1, 1, tzinfo=timezone.utc),
    schedule=timedelta(minutes=15),
    catchup=False,
    is_paused_upon_creation=True,
    max_active_runs=1,
    dagrun_timeout=timedelta(minutes=10),
    default_args={"retries": 2, "retry_delay": timedelta(seconds=15)},
    tags=["se363", "replay", "synthetic"],
) as dag:

    @task
    def check_services():
        result = api_get("/health")
        if result.get("status") != "ok":
            raise RuntimeError("Project API is not ready")

    @task
    def validate_input():
        return validate_sample(
            "/opt/project/data/samples/demo.jsonl", get_current_context()["run_id"]
        )

    @task
    def publish_to_kafka(manifest):
        return publish_sample(manifest)

    @task
    def summarize_run(manifest):
        summary = completion_summary(manifest)
        if not summary["complete"]:
            raise RuntimeError("Pipeline is no longer complete")
        return summary

    validated = validate_input()
    check_services() >> validated
    published = publish_to_kafka(validated)
    completed = PythonSensor(
        task_id="wait_for_pipeline",
        python_callable=pipeline_complete,
        op_kwargs={"manifest": published},
        mode="reschedule",
        poke_interval=10,
        timeout=240,
    )
    completed >> summarize_run(published)
