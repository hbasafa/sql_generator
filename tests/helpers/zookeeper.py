from src.app import settings
from tests.helpers.docker_helper import DockerHelper
import socket
import pytest


class ZookeeperServer(DockerHelper):
    """
    A helper class for managing a ZooKeeper Docker container.
    """

    def __init__(self, image=settings.TEST_ZOOKEEPER_IMAGE_NAME,
                 container_name=settings.TEST_ZOOKEEPER_CONTAINER_NAME,
                 host=settings.TEST_ZOOKEEPER_HOST,
                 port=settings.TEST_ZOOKEEPER_PORT):
        """
        Initializes the ZooKeeper object.
        """
        super().__init__(image_name=image, container_name=container_name, host=host, port=port)

    def get_env_vars(self):
        return {"ALLOW_ANONYMOUS_LOGIN": "yes",
                "ZOO_4LW_COMMANDS_WHITELIST": "ruok,stat,conf"}

    def check_container(self, timeout=settings.TEST_TIMEOUT):
        try:
            with socket.create_connection((self.host, self.port), timeout=timeout) as sock:
                return
        except Exception as e:
            pytest.fail(f"ZooKeeper did not become ready in time: {e}")

    def run(self, **kwargs):
        super().run(**kwargs)
        self.check_container()
