FROM python:3.8-slim

# Install netcat-openbsd
RUN apt-get update && apt-get install -y netcat-openbsd

WORKDIR /app

# Copy both applications into the Docker image
COPY requirements.txt .
COPY schema_loader.py .
COPY websocket_client.py .
COPY load-schema-and-start-websocket-client.sh .
COPY btcusdt-kline-value_event.avsc .
COPY wait-for-it.sh .

RUN pip install --no-cache-dir -r requirements.txt

RUN chmod +x wait-for-it.sh
RUN chmod +x load-schema-and-start-websocket-client.sh

CMD ["/app/load-schema-and-start-websocket-client.sh"]