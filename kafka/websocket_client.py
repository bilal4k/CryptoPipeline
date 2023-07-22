import asyncio
import json
import websockets
from confluent_kafka import Producer


# Kafka broker configuration
bootstrap_servers = '172.17.0.1:9092'

# Create Kafka producer instance
producer = Producer({'bootstrap.servers': bootstrap_servers})

# Topic to produce messages to
topic = 'btcusdt-kline'
subject = topic + '-value'

async def connect_websocket():
    uri = 'wss://stream.binance.com:9443/ws/btcusdt@kline_1m'  # Binance WebSocket URL

    try:
        async with websockets.connect(uri) as websocket:
            while True:
                message = await websocket.recv()
                json_message = json.loads(message)
                candle = json_message['k']
                is_candle_closed = candle['x']
                if is_candle_closed:
                    producer.produce(topic, value=message)
                    producer.flush()

                    print('Received message:', message)
    except websockets.exceptions.ConnectionClosedError as e:
        print('WebSocket connection closed unexpectedly:', str(e))
    except Exception as e:
        print('Error connecting to the WebSocket server:', str(e))

# Start the WebSocket connection
asyncio.get_event_loop().run_until_complete(connect_websocket())