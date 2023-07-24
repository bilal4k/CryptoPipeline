import json
import logging

# 3rd party library imported
import asyncio
import websockets
from confluent_kafka import SerializingProducer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.schema_registry import Schema


init_string = 'data: '
source_ws = 'wss://stream.binance.com:9443/ws/btcusdt@kline_1m'
kafka_url = 'kafka:9092'
schema_registry_url = 'http://schemaregistry:8085'
kafka_topic = 'btcusdt-kline'
schema_registry_subject = f"{kafka_topic}-value"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def connect_websocket(source_ws, producer):
    try:
        async with websockets.connect(source_ws) as websocket:
            while True:
                message = await websocket.recv()
                json_message = json.loads(message)
                candle = json_message['k']
                is_candle_closed = candle['x']
                if is_candle_closed:
                    try:
                        producer.produce(
                            kafka_topic, value=json_message, on_delivery=delivery_report)
                        producer.flush()
                        logger.info('Sent message: %s', json_message)
                    except Exception as e:
                        logger.error(
                            'Cannot send message: %s . Error : %s', json_message, str(e))

    except websockets.exceptions.ConnectionClosedError as e:
        logger.error('WebSocket connection closed unexpectedly: %s', str(e))
    except Exception as e:
        logger.error('Error connecting to the WebSocket server: %s', str(e))


async def avro_producer(source_ws, kafka_url, schema_registry_url, schema_registry_subject):
    # schema registry
    sr, latest_version = get_schema_from_schema_registry(
        schema_registry_url, schema_registry_subject)

    
    value_avro_serializer = AvroSerializer(schema_registry_client=sr,
                                           schema_str=latest_version.schema.schema_str,
                                           conf={
                                               'auto.register.schemas': False
                                           }
                                           )
    logger.info('Schema {} will be used'.format(
        latest_version.schema.schema_str))
    # Kafka Producer
    producer = SerializingProducer({
        'bootstrap.servers': kafka_url,
        'security.protocol': 'plaintext',
        'value.serializer': value_avro_serializer,
        'delivery.timeout.ms': 120000,  # set it to 2 mins
        'enable.idempotence': 'true'
    })

    await connect_websocket(source_ws, producer)

def delivery_report(errmsg, msg):
    if errmsg is not None:
        logger.error(
            "Delivery failed for Message: {} : {}".format(msg.key(), errmsg))
        return
    logger.info('Message: {} successfully produced to Topic: {} Partition: [{}] at offset {}'.format(
        msg.key(), msg.topic(), msg.partition(), msg.offset()))


def get_schema_from_schema_registry(schema_registry_url, schema_registry_subject):
    sr = SchemaRegistryClient({'url': schema_registry_url})
    latest_version = sr.get_latest_version(schema_registry_subject)

    return sr, latest_version


def register_schema(schema_registry_url, schema_registry_subject, schema_str):
    sr = SchemaRegistryClient({'url': schema_registry_url})
    schema = Schema(schema_str, schema_type="AVRO")
    schema_id = sr.register_schema(
        subject_name=schema_registry_subject, schema=schema)

    return schema_id


def update_schema(schema_registry_url, schema_registry_subject, schema_str):
    sr = SchemaRegistryClient({'url': schema_registry_url})
    versions_deleted_list = sr.delete_subject(schema_registry_subject)
    logger.info(f"versions of schema deleted list: {versions_deleted_list}")

    schema_id = register_schema(
        schema_registry_url, schema_registry_subject, schema_str)
    return schema_id


if __name__ == "__main__":
    logger.info("Connecting to Kafka Producer")
    # Start the WebSocket connection
    asyncio.run(avro_producer(source_ws, kafka_url, schema_registry_url,
                              schema_registry_subject))
