from django.core.management.base import BaseCommand
from confluent_kafka import Consumer, KafkaException
from confluent_kafka.cimpl import KafkaError
from django.conf import settings


class Command(BaseCommand):
    help = "Consume messages from Kafka"

    def handle(self, *args, **kwargs):
        conf = {
            "bootstrap.servers": settings.KAFKA_BOOTSTRAP_SERVERS,
            "group.id": "mygroup",
            "auto.offset.reset": "earliest",
        }
        consumer = Consumer(**conf)
        consumer.subscribe([settings.MESSAGE_TOPIC])
        try:
            while True:
                msg = consumer.poll(timeout=1.0)
                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        continue
                    else:
                        raise KafkaException(msg.error())
                print("Received message: {}".format(msg.value().decode("utf-8")))
        except KeyboardInterrupt:
            pass
        finally:
            consumer.close()
