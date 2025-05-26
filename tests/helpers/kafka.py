from src.app import settings
from tests.helpers.docker_helper import DockerHelper
from confluent_kafka.admin import AdminClient
from urllib.parse import urlparse
import pytest


class KafkaServer(DockerHelper):
    """
    A helper class for managing a Kafka Docker container.
    """

    def __init__(self, image=settings.TEST_KAFKA_IMAGE_NAME,
                 container_name=settings.TEST_KAFKA_CONTAINER_NAME,
                 host=settings.TEST_KAFKA_HOST,
                 port=settings.TEST_KAFKA_PORT):
        """
        Initializes the Kafka object.
        """
        super().__init__(image_name=image, container_name=container_name, host=host, port=port)

    def get_env_vars(self):
        return {
            "KAFKA_BROKER_ID": "1",
            "KAFKA_CFG_ZOOKEEPER_CONNECT": f"{settings.TEST_ZOOKEEPER_CONTAINER_NAME}:{settings.TEST_ZOOKEEPER_PORT}",
            "KAFKA_CFG_LISTENERS": f"PLAINTEXT://:{self.port}",
            "KAFKA_CFG_ADVERTISED_LISTENERS": f"{settings.TEST_KAFKA_BROKER_URL}",
            "ALLOW_PLAINTEXT_LISTENER": "yes",
        }

    def check_container(self, timeout=settings.TEST_TIMEOUT):
        try:
            admin = AdminClient({'bootstrap.servers': f"{self.host}:{self.port}"})
            metadata = admin.list_topics(timeout=timeout)
        except Exception as e:
            pytest.fail(f"Kafka container is not working: {e}")

    def run(self, **kwargs):
        super().run(**kwargs)
        self.check_container()
