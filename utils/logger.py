import logging
from kafka import KafkaProducer

class LogService:
    def __init__(self, kafka_servers, kafka_topic):
        self.kafka_servers = kafka_servers
        self.kafka_topic = kafka_topic
        self.producer = KafkaProducer(bootstrap_servers=self.kafka_servers)

    def log(self, message):
        try:
            self.producer.send(self.kafka_topic, value=message.encode('utf-8'))
        except Exception as e:
            # Handle any exceptions or errors that may occur during logging
            logging.error(f"Failed to log message to Kafka: {e}")

    def close(self):
        self.producer.close()

# Example usage:
if __name__ == "__main__":
    kafka_servers = 'localhost:9092'  # Replace with your Kafka broker
    kafka_topic = 'django_log'  # Replace with your Kafka topic

    log_service = LogService(kafka_servers, kafka_topic)
    
    try:
        log_service.log("This is a test log message.")
    finally:
        log_service.close()

