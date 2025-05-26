# Given the db_schema, generate sample data for each table
import os
import json
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from src.app import bootstrap
bootstrap.init()

from src.app import settings
from src.llm import llm
from src.logging.log_manager import logger


def generate_sample_data(db_schema: list) -> dict:
    # Initialize an empty dictionary to store the generated data
    generated_data = {}

    # Iterate over each table in the schema
    for table_info in db_schema:
        table_name = table_info["name"]
        logger.info(f"Generating sample data for table: {table_name}")

        # Generate sample data for the current table
        try:
            res = llm.prompt_for_data(table_info)
            generated_data[table_name] = res
        except Exception as e:
            logger.error(f"Error generating sample data for table {table_name}: {e}")
            continue

    return generated_data


def save_data(data):
    json.dump(data, open(os.path.join(settings.APP_ROOT, settings.TEST_DATA_PATH), "w"))


def generate_table_data() -> list:
    db_schema = json.load(open(os.path.join(settings.APP_ROOT, settings.DB_SCHEMA_PATH)))
    data = generate_sample_data(db_schema)
    save_data(data)


# TODO: Implement the logic to generate sample data for a table using llm


if __name__ == '__main__':
    generate_table_data()