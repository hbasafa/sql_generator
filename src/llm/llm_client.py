import os
import json
from openai import OpenAI, OpenAIError
from src.app import settings
from src.app.dto_models import QueryResponse
from src.logging.log_manager import logger
from src.llm.models import SQLPair
from langchain_openai import ChatOpenAI
from src.llm.prompting import Prompting
from langchain.chat_models import init_chat_model


class LLMClient:

    def __init__(self):

        logger.info("Loading OpenAI API Key & Client...")

        self.base_url = settings.LLM_BASE_URL
        self.model_name = settings.LLM_MODEL_NAME
        self.max_tokens = settings.LLM_MAX_TOKENS
        self.temprerature = settings.LLM_TEMPERATURE

        self.client = self.create_client()

    def create_client(self):
        return ChatOpenAI(api_key=os.environ.get("LLM_OPENAI_API_KEY", None),
                          base_url=self.base_url,
                          max_completion_tokens=self.max_tokens,
                          temperature=self.temprerature,
                          model=self.model_name)

    def get_context(self, relevant_schema):
        logger.debug("Getting context from relevant schema...")
        return "\n".join([str(s) for s in relevant_schema])

    def prompt_for_greeting(self):
        logger.info("Prompting for greeting...")
        prompt = Prompting.create_messages(Prompting.TEMPLATE_GREETING)
        try:
            response = self.client.invoke(prompt)
        except OpenAIError as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise e
        return response


    def prompt_for_sql(self, user_query: str, relevant_schema: list) -> QueryResponse:
        logger.info("Prompting for SQL query...")

        # Check if relevant_schema is empty
        if not relevant_schema:
            logger.warning("Relevant schema is empty. Returning default response.")
            return QueryResponse(response="No relevant schema found.")

        # Construct context from relevant schema
        logger.debug(f"Relevant schema: {relevant_schema}")
        context = self.get_context(relevant_schema)
        logger.debug(f"Context: {context}")
        prompt = Prompting.create_messages(Prompting.TEMPLATE_SQL_GENERATION, user_query=user_query, context=context)
        logger.debug(f"Prompt: {prompt}")

        # Generate SQL query using OpenAI API
        try:
            # Combine query and schema context
            logger.debug(f"Generating response...")
            response = self.client.with_structured_output(QueryResponse).invoke(prompt)
            logger.debug(f"Response: {response}")
        except OpenAIError as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise e

        return response


    def prompt_for_pairs(self, table_info):
        logger.info("Prompting for pairs...")

        context = table_info
        prompt = Prompting.create_messages(Prompting.TEMPLATE_SQL_PAIRS, context=context)
        logger.debug(f"Prompt: {prompt}")

        try:
            response = self.client.with_structured_output(SQLPair).invoke(prompt)
        except OpenAIError as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise e

        return response


    def prompt_for_data(self, table_info):
        logger.info("Prompting for data...")

        context = table_info
        prompt = Prompting.create_messages(Prompting.TEMPLATE_DATA_SAMPLES, context=context)
        logger.debug(f"Prompt: {prompt}")

        try:
            response = self.client.invoke(prompt)
            response = json.loads(response.choices[0].message.content)
        except OpenAIError as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise e
        except json.JSONDecodeError as e:
            logger.error(f"JSON decoding error: {str(e)}")
            raise e

        return response
