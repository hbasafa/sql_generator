import requests
import json
import os
from src.app import settings
from src.logging.log_manager import logger


def crawl_schemas():
    # Fetch subjects, extract schemas, and save them
    logger.info(f"Start crawling schemas...")
    subjects = fetch_subjects()
    schemas = extract_schemas(subjects)
    save_schemas(schemas)
    logger.info(f"DB Schema file generated at {settings.DB_SCHEMA_PATH}")


def fetch_subjects():
    # Fetch subjects from DB
    subjects = requests.get(settings.DB_ENDPOINT).json()
    if subjects:
        logger.info(f"Found {len(subjects)} subjects.")
    else:
        logger.warning("No subjects found.")
        logger.warning("Please check the DB_ENDPOINT in settings.py.")
    return subjects


def extract_schemas(subjects):
    # Extract schemas from subjects
    schemas = []
    for s in subjects:
        endpoint = f"{settings.DB_ENDPOINT}/{s}/versions/latest/schema"
        schema = requests.get(endpoint).json()
        schemas.append(schema)
        logger.info(f"Fetched schema for {s}.")
        logger.debug(f"Schema: {schema}")
    return schemas


def save_schemas(schemas):
    # Save schemas to a file
    json.dump(schemas, open(os.path.join(settings.APP_ROOT, settings.DB_SCHEMA_PATH), "w"))
    logger.info(f"Saved schemas to {settings.DB_SCHEMA_PATH}.")
