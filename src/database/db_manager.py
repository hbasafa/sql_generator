import json
import os
from src.app import settings
from src.logging.log_manager import logger


def get_schema():
    return fetch_schema()


def fetch_schema():
    schema = {}
    schema_path = os.path.join(settings.APP_ROOT, settings.DB_SCHEMA_PATH)
    logger.info(f"Loading schema from {schema_path}...")
    schema = load_schema(schema_path)
    return schema


def load_schema(path):
    schema = {}
    try:
        schema = json.load(open(path, "r"))
        logger.info(f"Loaded schemas from {path}.")
    except FileNotFoundError:
        logger.error(f"Schema file not found at {path}")
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON in schema file at {path}")
    return schema