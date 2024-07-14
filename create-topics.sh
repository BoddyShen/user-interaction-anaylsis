#!/bin/bash

# Wait for Kafka to be ready
echo "Waiting for Kafka to be ready..."
cub kafka-ready -b localhost:9092 1 20

# Create the topic
echo "Creating Kafka topic 'user_interactions'..."
kafka-topics --create --topic user_interactions --bootstrap-server localhost:9092 --partitions 3 --replication-factor 1

echo "Topic 'user_interactions' created."