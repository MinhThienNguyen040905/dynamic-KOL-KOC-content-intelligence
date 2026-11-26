FROM apache/airflow:3.1.8-python3.11
# Airflow owns its dependency environment. Only add the producer client needed by DAG tasks.
RUN pip install --no-cache-dir "apache-airflow==3.1.8" "confluent-kafka==2.6.1"
RUN mkdir -p /opt/airflow/auth

