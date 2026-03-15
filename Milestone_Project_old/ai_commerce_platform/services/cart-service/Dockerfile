FROM python:3.11-slim

WORKDIR /app

COPY services/common-lib /tmp/common-lib
RUN pip install --no-cache-dir -U pip && pip install --no-cache-dir /tmp/common-lib

COPY services/cart-service/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY services/cart-service/app /app/app

EXPOSE 8003
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8003"]
