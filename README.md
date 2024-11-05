
# Kafka Django Logging

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Installation

1. Clone the repository:
    ```sh
    git clone <repository_url>
    cd kafka_django_logging
    ```

2. Start the services using Docker Compose:
    ```sh
    docker-compose up
    ```

    This will start Django, Kafka, and Zookeeper.

### Setting Up Kafka Topic

1. Bash into the Kafka container:
    ```sh
    docker exec -it <kafka_container_id> /bin/bash
    ```

2. Create a Kafka topic:
    ```sh
    kafka-topics --create --topic <topic_name> --bootstrap-server kafka:9092 --partitions 1 --replication-factor 1
    ```

    Replace `<topic_name>` with the topic name specified in your environment variables.

### Example Environment Variables

```env
SECRET_KEY = <YOUR_SECRET_KEY>
KAFKA_BOOTSTRAP_SERVERS = kafka:9092
MESSAGE_TOPIC = <KAFKA_TOPIC_NAME>
```

### Consuming Messages

You can consume messages using one of the following methods:

1. **Within the Kafka container:**
    - Bash into the Kafka container:
        ```sh
        docker exec -it <kafka_container_id> /bin/bash
        ```
    - Consume messages:
        ```sh
        kafka-console-consumer --bootstrap-server localhost:9092 --topic <topic_name>
        ```

2. **Within the Django container:**
    - Bash into the Django container:
        ```sh
        docker exec -it <django_container_id> /bin/bash
        ```
    - Run the Django management command:
        ```sh
        python manage.py consume_logs
        ```

Replace `<kafka_container_id>` and `<django_container_id>` with the respective container IDs.