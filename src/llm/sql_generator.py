from src.llm.llm_client import LLMClient
from src.logging.log_manager import logger
from src.app.dto_models import QueryRequest, QueryResponse
from src.database.schema_db import SchemaDB


class SQLGenerator:

    def __init__(self):
        self.llm = LLMClient()
        self.schema_db = SchemaDB()

    def generate_sql_query(self, user_query: QueryRequest) -> QueryResponse:
        # Retrieve relevant schema
        logger.debug("Retrieving relevant schema...")
        relevant_schema = self.schema_db.retrieve_relevant_schema(user_query)
        logger.debug(f"Relevant schema: {relevant_schema}")

        # Generate SQL query
        logger.debug("Generating SQL query...")
        response = self.llm.prompt_for_sql(user_query, relevant_schema)
        logger.debug(f"Generated SQL query: {response}")

        return response

    def init_db(self):
        self.schema_db.init_db()

