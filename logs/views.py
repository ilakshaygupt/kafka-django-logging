import json
import logging
from confluent_kafka import Producer
from django.conf import settings
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework import status

# Setup Kafka producer (this can be moved to settings or an external service file if needed)
kafka_conf = {
    "bootstrap.servers": settings.KAFKA_BOOTSTRAP_SERVERS,
    "client.id": "django_logger",
}
producer = Producer(kafka_conf)
kafka_topic = settings.MESSAGE_TOPIC

# Configure logging
logger = logging.getLogger(__name__)


class CreateUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            self.log_to_kafka(
                {
                    "message": f"User '{user.username}' created successfully.",
                    "level": "INFO",
                    "user_id": user.id,
                }
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        self.log_to_kafka(
            {
                "message": "User creation failed.",
                "level": "ERROR",
                "errors": serializer.errors,
            }
        )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def log_to_kafka(self, log_data):
        """
        Send log data to Kafka.
        """
        try:
            producer.produce(kafka_topic, json.dumps(log_data).encode("utf-8"))
            producer.flush()
            logger.info(f"Sent log to Kafka: {log_data}")
        except Exception as e:
            logger.error(f"Failed to log to Kafka: {str(e)}")


# to consume bash into confluentinc/cp-kafka:latest using < docker exec -it 8531497ae1f2  /bin/bash >
# can consume using kafka-console-consumer --bootstrap-server localhost:9092 --topic <topic>
