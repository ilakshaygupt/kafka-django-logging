#!/bin/sh

# Wait for Kafka to be ready
echo "Waiting for Kafka to be ready..."
sleep 10

# Create Kafka topic if it doesn't exist
echo "Creating Kafka topic..."
kafka-topics --bootstrap-server kafka:9092 --create --if-not-exists --topic django_mog --partitions 1 --replication-factor 1
echo "Kafka topic created or already exists."

# Run the Django server
echo "Starting Django server..."
exec python manage.py runserver 0.0.0.0:8000
