
# App settings
APP_HOST = "0.0.0.0"
APP_PORT = 9000
APP_DEBUG = True
APP_ROOT = "."

# LLM settings
LLM_MODEL_NAME = "gpt-4o-mini"
LLM_TEMPERATURE = 0.8
LLM_MAX_TOKENS = 512
LLM_BASE_URL = "https://api.openai.com/v1/"
LLM_TEMPLATES_PATH = "configs/app/prompt_templates.yaml"

# VectorDB settings
VDB_TOP_K = 2
VDB_MODEL = "all-MiniLM-L6-v2"

# Trino Connection Config
TRINO_HOST = "http://localhost"
TRINO_PORT = 9080
TRINO_USER = "root"
TRINO_PASSWORD = ""
TRINO_DATABASES = ["postgresql.public", "mongodb.admin"]

# DB Dump file
DB_SCHEMA_PATH = "data/db_schema.json"
DB_ENDPOINT = "http://172.32.16.31:30900/subjects"

# Test configs
TEST_PAIRS_PATH = "data/pairs.json"
TEST_DATA_PATH = "data/samples.json"
TEST_LLM_IMAGE_NAME =  "ollama/ollama:0.6.6-gemma3-1b"
TEST_LLM_MODEL_NAME = "gemma3:1b"
TEST_LLM_CONTAINER = "ollama_test"
TEST_LLM_CONTAINER_PORT = 11434
TEST_LLM_HOST = "localhost"
TEST_LLM_BASE_URL = "http://localhost:11434/v1"
TEST_TIMEOUT = 15
TEST_NETWORK_NAME = "test_network"
TEST_ZOOKEEPER_IMAGE_NAME = "bitnami/zookeeper:3.9.1"
TEST_ZOOKEEPER_CONTAINER_NAME = "zookeeper_test"
TEST_ZOOKEEPER_PORT = 2181
TEST_ZOOKEEPER_HOST = "localhost"
TEST_KAFKA_IMAGE_NAME = "bitnami/kafka:3.6.1"
TEST_KAFKA_CONTAINER_NAME = "kafka_test"
TEST_KAFKA_PORT = 9092
TEST_KAFKA_HOST = "localhost"
TEST_KAFKA_BROKER_URL = "PLAINTEXT://kafka_test:9092"
TEST_KAFKA_TOPIC = "test_topic"
TEST_SCHEMA_REGISTRY_IMAGE_NAME = "confluentinc/cp-schema-registry:7.5.0"
TEST_SCHEMA_REGISTRY_CONTAINER_NAME = "schema_registry_test"
TEST_SCHEMA_REGISTRY_PORT = 8081
TEST_SCHEMA_REGISTRY_HOST = "localhost"
TEST_DB_SCHEMA_PATH = "data/test_db_schema.json"
TEST_DB_ENDPOINT = f"{TEST_SCHEMA_REGISTRY_HOST}:{TEST_SCHEMA_REGISTRY_PORT}/subjects"

# Docker settings
DOCKER_ENV = ".env"

# Logging settings
DEFAULT_LOGGER = "app.sql_generator"
LOG_LEVEL = "DEBUG" if APP_DEBUG else "INFO"
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] [%(filename)s] %(name)s: %(message)s'
        },
        'custom_formatter': {
            'format': "%(asctime)s [%(processName)s: %(process)d] [%(threadName)s: %(thread)d] [%(levelname)s] [%(filename)s] %(name)s: %(message)s"
        },
    },
    'handlers': {
        'default': {
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',  # Default is stderr
        },
        'stream_handler': {
            'formatter': 'custom_formatter',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',  # Default is stderr
        },
        'file_handler': {
            'formatter': 'custom_formatter',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'app.log',
            'maxBytes': 1024 * 1024 * 1, # = 1MB
            'backupCount': 3,
        },
    },
    'loggers': {
        'uvicorn': {
            'handlers': ['default', 'file_handler'],
            'level': LOG_LEVEL,
            'propagate': False
        },
        'uvicorn.access': {
            'handlers': ['stream_handler', 'file_handler'],
            'level': LOG_LEVEL,
            'propagate': False
        },
        'uvicorn.error': {
            'handlers': ['stream_handler', 'file_handler'],
            'level': LOG_LEVEL,
            'propagate': False
        },
        'uvicorn.asgi': {
            'handlers': ['stream_handler', 'file_handler'],
            'level': LOG_LEVEL,
            'propagate': False
        },
        DEFAULT_LOGGER: {
            'handlers': ['default', 'file_handler'],
            'level': LOG_LEVEL,
            'propagate': False
        },
    },
}