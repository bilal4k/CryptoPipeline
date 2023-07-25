import time
import requests
import logging
import os

# Set up logging
logging.basicConfig(level=logging.INFO)

# Constant values
SCHEMA_REGISTRY_URL = os.getenv('SCHEMA_REGISTRY_URL')
SCHEMA_FILE_PATH = os.getenv('SCHEMA_FILE_PATH')
COMPATIBILITY_LEVEL = os.getenv('COMPATIBILITY_LEVEL')

def read_avro_schema(file_path):
    with open(file_path, 'r') as schema_file:
        avro_schema = schema_file.read().replace('"', '\\"').replace('\n', '\\n')
    return avro_schema


def load_avro_schema(avro_schema):
    url = f'{SCHEMA_REGISTRY_URL}/subjects/btcusdt-kline-value/versions'
    headers = {'Content-Type': 'application/vnd.schemaregistry.v1+json'}
    data = f'{{"schema": "{avro_schema}"}}'
    return requests.post(url, headers=headers, data=data)


def main():
    logging.info("Waiting for Schema Registry to start...")
    time.sleep(2)  # Adjust the delay if necessary

    logging.info(f"Reading schema from {SCHEMA_FILE_PATH}")
    avro_schema = read_avro_schema(SCHEMA_FILE_PATH)

    logging.info(f"Setting compatibility level to {COMPATIBILITY_LEVEL}...")
    url = f'{SCHEMA_REGISTRY_URL}/config'
    headers = {'Content-Type': 'application/vnd.schemaregistry.v1+json'}
    requests.put(url, headers=headers, data=COMPATIBILITY_LEVEL)

    response = load_avro_schema(avro_schema)

    if response.status_code == 200:
        logging.info("Schema successfully loaded.")
    else:
        logging.error(
            f"Failed to load schema. HTTP Response Code: {response.status_code}")
        logging.error("Response Body:")
        logging.error(response.text)


if __name__ == "__main__":
    main()
