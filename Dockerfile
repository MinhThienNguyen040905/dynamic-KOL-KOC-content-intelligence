FROM python:3.11.11-slim-bookworm
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 \
    JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64 \
    PYSPARK_PYTHON=python SPARK_LOCAL_IP=0.0.0.0
RUN apt-get update && apt-get install -y --no-install-recommends openjdk-17-jre-headless \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY pyproject.toml ./
RUN python -c "import tomllib,subprocess,sys; p=tomllib.load(open('pyproject.toml','rb'))['project']; subprocess.check_call([sys.executable,'-m','pip','install','--no-cache-dir',*p['dependencies'],*p['optional-dependencies']['spark']])"
COPY src ./src
RUN pip install --no-cache-dir --no-deps .
COPY data/samples ./data/samples
RUN mkdir -p /data/archive /data/checkpoints /tmp/ivy
EXPOSE 8000 8001
CMD ["uvicorn", "kol.api:app", "--host", "0.0.0.0", "--port", "8000"]

