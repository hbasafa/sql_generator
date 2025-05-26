import docker
import time
import requests
import pytest
import warnings
from src.app import settings
from tests.helpers.docker_helper import DockerHelper


class OllamaServer(DockerHelper):
    def __init__(self, image_name=settings.TEST_LLM_IMAGE_NAME,
                 container_name=settings.TEST_LLM_CONTAINER,
                 container_port=settings.TEST_LLM_CONTAINER_PORT,
                 model_name=settings.TEST_LLM_MODEL_NAME,
                 host=settings.TEST_LLM_HOST):
        super().__init__(image_name=image_name, container_name=container_name, host=host, port=container_port)
        self.model_name = model_name

    def run(self, **kwargs):
        super().run(**kwargs)
        self.check_service()

    def pull_model(self, max_retries=3, delay=2):
        retries = 0
        while retries < max_retries:
            try:
                self.exec_command(f"ollama pull {self.model_name}", tty=True, stdin=True, stdout=True, stderr=True)
                return
            except docker.errors.APIError as e:
                retries += 1
                with pytest.warns(UserWarning, match=f"Attempt {retries}/{max_retries} failed: {e}. Retrying..."):
                    warnings.warn(f"Attempt {retries}/{max_retries} failed: {e}. Retrying...", UserWarning)
                time.sleep(delay)

        pytest.fail(f"Model {self.model_name} could not be pulled after {max_retries} attempts.")

    def check_service(self, waiting_time=settings.TEST_TIMEOUT):
        for _ in range(waiting_time):
            try:
                r = requests.get(f"http://{self.host}:{self.port}", timeout=1)
                if r.status_code == 200:
                    break
            except requests.exceptions.RequestException or requests.ConnectionError:
                time.sleep(1)
        else:
            self.terminate()
            pytest.fail("Ollama server didn't start in time.")

