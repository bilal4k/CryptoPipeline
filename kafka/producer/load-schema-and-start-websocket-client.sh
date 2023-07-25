#!/bin/bash

# Run the schema_loader
python schema_loader.py

# Once the schema_loader has completed, run the websocket_client
python websocket_client.py