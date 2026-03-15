FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y default-jdk curl && rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/lib/jvm/default-java

COPY data-engineering/inventory_pipeline/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -U pip && pip install --no-cache-dir -r /app/requirements.txt

COPY data-engineering/inventory_pipeline/spark_job.py /app/spark_job.py
COPY src /app/src

CMD ["python", "spark_job.py"]
