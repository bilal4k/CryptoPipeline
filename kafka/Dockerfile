FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY websocket_client.py .

CMD ["python", "websocket_client.py"]