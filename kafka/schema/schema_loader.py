import time
import requests

# URL of the Schema Registry
SCHEMA_REGISTRY_URL = 'http://schemaregistry:8085'

# Path to the Avro schema file
SCHEMA_FILE_PATH = "btcusdt-kline-value_event.avsc"

def read_avro_schema(file_path):
    """
    Read the Avro schema from the provided file path.

    Args:
        file_path: Path to the Avro schema file

    Returns:
        A string containing the Avro schema
    """
    with open(file_path, 'r') as schema_file:
        avro_schema = schema_file.read().replace('"', '\\"').replace('\n', '\\n')
    return avro_schema

def load_avro_schema(avro_schema):
    """
    Load the Avro schema into the Schema Registry.

    Args:
        avro_schema: The Avro schema string to load

    Returns:
        The response from the Schema Registry
    """
    url = f'{SCHEMA_REGISTRY_URL}/subjects/btcusdt-kline-value/versions'
    headers = {'Content-Type': 'application/vnd.schemaregistry.v1+json'}
    data = f'{{"schema": "{avro_schema}"}}'
    return requests.post(url, headers=headers, data=data)

def main():
    """
    Main function to read the Avro schema, load it into the Schema Registry, 
    and handle the response.
    """
    print("Waiting for Schema Registry to start...")
    time.sleep(2)  # Adjust the delay if necessary

    print(f"Reading schema from {SCHEMA_FILE_PATH}")
    avro_schema = read_avro_schema(SCHEMA_FILE_PATH)

    print("Setting compatibility level to NONE...")
    url = f'{SCHEMA_REGISTRY_URL}/config'
    headers = {'Content-Type': 'application/vnd.schemaregistry.v1+json'}
    data = '{"compatibility": "NONE"}'
    requests.put(url, headers=headers, data=data)

    response = load_avro_schema(avro_schema)

    if response.status_code == 200:
        print("Schema successfully loaded.")
    else:
        print(
            f"Failed to load schema. HTTP Response Code: {response.status_code}")
        print("Response Body:")
        print(response.text)

if __name__ == "__main__":
    main()