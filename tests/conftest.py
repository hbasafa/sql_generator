import docker.errors
import pytest
import os
import logging
import docker
import time
import requests
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from tests.helpers.ollama import OllamaServer
from tests.helpers.schema_registry import SchemaRegistryServer
from tests.helpers.zookeeper import ZookeeperServer
from tests.helpers.kafka import KafkaServer
from tests.helpers.docker_helper import DockerHelper
from src.app import settings
from src.app.api import API
from src.database.schema_db import SchemaDB
from src.llm.sql_generator import SQLGenerator
from src.llm.prompting import Prompting


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@pytest.fixture(scope="session", autouse=True)
def global_setup():
    logger.info("[Setup] Running once before the whole test session")

    try:
        # Load environment variables from .env file
        load_dotenv(os.path.join(settings.APP_ROOT, settings.DOCKER_ENV), override=True)

        # Bootstrap
        logger.info("Bootstrapping...")
        Prompting.load_templates()

        # test time vars
        logger.info(f"Setting up the variables")
        settings.LLM_BASE_URL = settings.TEST_LLM_BASE_URL
        settings.LLM_MODEL_NAME = settings.TEST_LLM_MODEL_NAME
        settings.DB_ENDPOINT = settings.TEST_DB_ENDPOINT
        settings.DB_SCHEMA_PATH = settings.TEST_DB_SCHEMA_PATH

        # Cleanup environment before setting up
        logger.info("Cleaning up environment...")
        cleanup()

        # Create the network
        logger.info(f"Creating network {settings.TEST_NETWORK_NAME}...")
        DockerHelper.client.networks.create(settings.TEST_NETWORK_NAME, driver="bridge")

        # Ollama server
        logger.info(f"Starting Ollama server at {settings.TEST_LLM_HOST}:{settings.TEST_LLM_CONTAINER_PORT}...")
        ollama_server = OllamaServer()
        ollama_server.run(network=settings.TEST_NETWORK_NAME)
        logger.info(f"Ollama server started")

        # Zookeeper
        logger.info(f"Starting Zookeeper server at {settings.TEST_ZOOKEEPER_HOST}:{settings.TEST_ZOOKEEPER_PORT}...")
        zookeeper_server = ZookeeperServer()
        zookeeper_server.run(network=settings.TEST_NETWORK_NAME)
        logger.info(f"Zookeeper server started")

        # Kafka
        logger.info(f"Starting Kafka server at {settings.TEST_KAFKA_HOST}:{settings.TEST_KAFKA_PORT}...")
        kafka_server = KafkaServer()
        kafka_server.run(network=settings.TEST_NETWORK_NAME)
        logger.info(f"Kafka server started")

        # Schema Registry
        logger.info(f"Starting Schema Registry server at {settings.TEST_SCHEMA_REGISTRY_HOST}:{settings.TEST_SCHEMA_REGISTRY_PORT}...")
        schema_registry_server = SchemaRegistryServer()
        schema_registry_server.run(network=settings.TEST_NETWORK_NAME)
        logger.info(f"Schema Registry server started")

        # Initialize schema registry
        url = f"http://{settings.TEST_SCHEMA_REGISTRY_HOST}:{settings.TEST_SCHEMA_REGISTRY_PORT}/subjects/product-value/versions"
        schema = {
            "schema": '{"type": "record", "name": "Product", "fields": [{"name": "id", "type": "int"}, {"name": "name", "type": "string"}]}'
        }
        response = requests.post(url, json=schema)
        assert response.status_code == 200

        yield

        logger.info("[Teardown] Terminating Docker containers...")

        # Terminate Docker containers
        ollama_server.terminate()
        zookeeper_server.terminate()
        kafka_server.terminate()
        schema_registry_server.terminate()
        DockerHelper.client.networks.get(settings.TEST_NETWORK_NAME).remove()
    except Exception as e:
        logger.error(f"Error during global setup: {e}")
        pytest.fail(f"Error during global setup: {e}")
    finally:
        logger.info("[Teardown] Running once after the whole test session")
        cleanup()


@pytest.fixture(scope="session")
def schema_registry_url():
    return f"http://{settings.TEST_SCHEMA_REGISTRY_HOST}:{settings.TEST_SCHEMA_REGISTRY_PORT}"


@pytest.fixture(scope="session")
def test_client():
    #TODO bootstrap?
    sdb = SchemaDB()
    schemas = ["test_schema1", "test_schema2"]
    sdb.set_schema_context(schemas)
    e = sdb.get_schema_embeddings(schemas)
    sdb.add_index(e)

    sql_generator = SQLGenerator()
    sql_generator.schema_db = sdb

    api = API()
    api.sql_generator = sql_generator
    app = api.get_app()
    return TestClient(app)


def cleanup():
    # Clean up containers
    test_containers = DockerHelper.client.containers.list(all=True, filters=DockerHelper.get_filters())
    for c in test_containers:
        c.stop()
        c.remove(force=True)

    # Cleanup the network
    try:
        DockerHelper.client.networks.get(settings.TEST_NETWORK_NAME).remove()
    except docker.errors.NotFound:
        pass
