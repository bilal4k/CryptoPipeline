FROM python:3.9-slim

WORKDIR /app

COPY schema_loader.py /app/
COPY btcusdt-kline-value_event.avsc /app/
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "schema_loader.py"]