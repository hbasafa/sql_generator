import docker
import docker.errors
import pytest
from abc import ABC


class DockerHelper(ABC):
    client = docker.from_env()

    def __init__(self, image_name, container_name, port, host):
        self.image_name = image_name
        self.container_name = container_name
        self.port = port
        self.host = host

    def get_container(self):
        return self.client.containers.get(self.container_name)

    def run(self, **kwargs):
        if not self.check_image_exists(self.image_name):
            self.pull_image()
        self.cleanup_container()
        self.run_container(**kwargs)

    def terminate(self):
        container = self.get_container()
        container.kill()
        container.remove()

    def pull_image(self):
        self.client.images.pull(self.image_name)

    def run_container(self, **kwargs):
        self.client.containers.run(
                self.image_name,
                name=self.container_name,
                detach=True,
                ports={f"{self.port}/tcp": self.port},
                hostname=self.host,
                tty=True,
                environment=self.get_env_vars(),
                labels=self.get_labels(),
                **kwargs
            )

    def exec_command(self, command, *args, **kwargs):
        container = self.get_container()
        result = container.exec_run(command, *args, **kwargs)
        return result.output.decode('utf-8')

    def cleanup_container(self):
        try:
            container = self.get_container()

            if container.status == "running":
                container.kill()

            container.remove(force=True)

        except docker.errors.NotFound:
            pass
        except docker.errors.APIError as e:
            pytest.fail(f"Error during container cleanup: {e.explanation}")

    def get_env_vars(self):
        return None

    @staticmethod
    def get_labels():
        return {"pytest-test": "true"}

    @staticmethod
    def get_filters():
        return {"label": "pytest-test=true"}

    def check_image_exists(self, image_name):
        try:
            self.client.images.get(image_name)
            return True
        except docker.errors.NotFound:
            return False
        except Exception as e:
            return False
