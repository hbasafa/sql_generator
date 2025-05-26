import pytest
import docker
import time
import requests
from docker.errors import ContainerError, ImageNotFound
from tests.helpers.docker_helper import DockerHelper
from src.app import settings


class SchemaRegistryServer(DockerHelper):
    """
    A helper class for managing a Confluent Schema Registry Docker container.
    """

    def __init__(self,
                 image=settings.TEST_SCHEMA_REGISTRY_IMAGE_NAME,
                 container_name=settings.TEST_SCHEMA_REGISTRY_CONTAINER_NAME,
                 host=settings.TEST_SCHEMA_REGISTRY_HOST,
                 port=settings.TEST_SCHEMA_REGISTRY_PORT,
                 ):
        """
        Initializes the SchemaRegistry object.
        """
        super().__init__(image_name=image, container_name=container_name, host=host, port=port)

    def get_env_vars(self):
        return {
            "SCHEMA_REGISTRY_HOST_NAME": f"{self.container_name}",
            "SCHEMA_REGISTRY_LISTENERS": f"http://0.0.0.0:{self.port}",
            "SCHEMA_REGISTRY_KAFKASTORE_BOOTSTRAP_SERVERS": f"{settings.TEST_KAFKA_BROKER_URL}",
            "SCHEMA_REGISTRY_KAFKASTORE_CONNECTION_URL": f"{settings.TEST_ZOOKEEPER_CONTAINER_NAME}:{settings.TEST_ZOOKEEPER_PORT}",
            }

    def run(self, **kwargs):
        super().run(**kwargs)
        self.check_container()

    def check_container(self, timeout=settings.TEST_TIMEOUT):
        url = f"http://{self.host}:{self.port}/subjects"
        start_time = time.time()

        while time.time() - start_time < timeout:
            try:
                response = requests.get(url, timeout=2)
                if response.status_code == 200:
                    return
            except requests.exceptions.RequestException as e:
                time.sleep(1)

        pytest.fail("Schema Registry did not become ready in time.")
