# Build the Docker Compose setup
build-up:
	docker compose down --volumes --remove-orphans
	docker compose build
	docker compose up -d

# Start the Docker Compose setup in detached mode
up:
	docker compose up -d

# Stop and remove all Docker containers and volumes
down:
	docker-compose down --volumes --remove-orphans


ws-log:
	docker-compose logs -f websocket_client

schema-log:
	docker-compose logs -f schema_loader



.PHONY: build-up up down ws-log schema-log