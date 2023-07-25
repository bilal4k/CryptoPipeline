# CryptoPipeline

<div align="center">

<img src="./doc/imgs/cryptoPipelineLogo.png" width="200"/>
  <div> </div>
  <div align="center">
    <b><font size="5">CryptoPipeline</font></b>
    <div> </div>
  </div>
</div>

## Introduction

CryptoPipeline is an open-source project focused on importing and processing cryptocurrency data. It provides a set of tools and scripts to facilitate the data engineering workflow for cryptocurrency enthusiasts and researchers.

## 🚧🤪 Work in Progress - Proceed with Laughter! 🚧🤪

Welcome to the marvelous world of this work-in-progress masterpiece! Here lies the wacky realm of code and chaos, where bugs and jokes coexist in perfect harmony. Please fasten your seatbelts, buckle up your funny bones, and prepare for a wild ride through this hilarious README (to come).

## Architecture Overview

CryptoPipeline employs a multi-service architecture, utilizing Docker Compose to manage and orchestrate the various components. The main components of the architecture include:

1. **Zookeeper**:
   A service responsible for maintaining Kafka cluster metadata.

2. **Kafka**:
   The core of the architecture, Kafka is a distributed event streaming platform used for message processing.

3. **Schema Registry**:
   Manages Avro schemas for data serialization and deserialization.

4. **WebSocket Client**:
   A custom-built WebSocket client that produces data to Kafka based on user-defined configurations.

5. **Kafka UI**:
   A web-based user interface for monitoring and managing Kafka topics.

6. **Kafka Init Topics**:
   A utility service used to initialize Kafka topics on startup.

## Prerequisites

Before running CryptoPipeline, ensure you have the following prerequisites installed on your system:

- Docker
- Docker Compose

## Getting Started

To set up and run CryptoPipeline, follow these steps:

1. Clone the repository:

```bash
    git clone https://github.com/bilal4k/CryptoPipeline.git
    cd CryptoPipeline
```

2. Build and start the Docker containers using Docker Compose:

```bash
    cd kafka && cp .env.dist .env
    make build-up
```

Wait for the services to start. Once ready, you can access the Kafka UI at http://localhost:8080.

## Future Roadmap

We have exciting plans for the future of CryptoPipeline! The following are some of the features and improvements we are considering:

- Building a Data Warehouse Testing Environment: We aim to develop a robust data warehouse testing environment to ensure data accuracy and consistency.

- Enhanced Analytics and Insights: We plan to implement advanced analytics capabilities, allowing users to gain valuable insights from the processed cryptocurrency data.

Stay tuned for updates as we continue to evolve and expand CryptoPipeline to meet the needs of cryptocurrency enthusiasts and researchers.