FROM python:3.11-slim

WORKDIR /app

COPY services/common-lib /tmp/common-lib
RUN pip install --no-cache-dir -U pip && pip install --no-cache-dir /tmp/common-lib

COPY services/api-gateway/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY services/api-gateway/app /app/app

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
