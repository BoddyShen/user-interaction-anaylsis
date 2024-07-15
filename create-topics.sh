#!/bin/bash

# Wait until Kafka is reachable
cub kafka-ready -b kafka:9092 1 20

# Create the topic
echo "Creating Kafka topic 'user_interactions'..."
kafka-topics --create --topic user_interactions --bootstrap-server kafka:9092 --partitions 3 --replication-factor 1

echo "Topic 'user_interactions' created."
