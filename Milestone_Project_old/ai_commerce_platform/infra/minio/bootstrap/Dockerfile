FROM python:3.11-slim

WORKDIR /bootstrap

RUN pip install --no-cache-dir -U pip boto3==1.40.17

COPY infra/minio/bootstrap/seed_inventory.py /bootstrap/seed_inventory.py

CMD ["python", "seed_inventory.py"]
