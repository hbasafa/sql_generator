import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from src.app import settings
from src.logging.log_manager import logger
from src.database.schema_db import SchemaDB
from src.llm.llm_client import LLMClient
from src.database.trinodb import TrinoDB


def init():
    #TODO: Seprate checking and initializing

    # Load environment variables from .env file
    logger.info("Loading environment variables...")
    load_dotenv(os.path.join(settings.APP_ROOT, settings.DOCKER_ENV), override=True)

    # Check db_schema
    logger.info("Checking DB Schema...")
    # check_db_schema()

    # Check LLM API
    logger.info("Checking LLM API...")
    check_llm_api()

    # Check Embedding model
    logger.info("Checking Embedding model...")
    check_embedding_model()

    # Check Vector DB
    logger.info("Checking Vector DB...")
    check_vector_db()

    # Check Trino API
    logger.info("Checking Trino API...")
    check_trino_api()


def check_db_schema():
    # Check if DB_SCHEMA_PATH is set
    if not settings.DB_SCHEMA_PATH:
        logger.error("DB_SCHEMA_PATH is not set. Please set it in settings.py.")
        exit(1)

    # Run the crawler to generate the schema file
    logger.info("Running the crawler to generate the schema file.")
    from src.database import crawler
    crawler.crawl_schemas()
    logger.debug("Crawler finished.")

    # Check if DB_SCHEMA file exists
    if os.path.exists(settings.DB_SCHEMA_PATH):
        logger.info(f"DB Schema file found at {settings.DB_SCHEMA_PATH}")
    else:
        logger.warning(f"DB Schema file not found at {settings.DB_SCHEMA_PATH}")


def check_llm_api():
    # Check if LLM_API_URL is set
    if not os.environ.get("LLM_OPENAI_API_KEY"):
        logger.error("LLM_OPENAI_API_KEY is not set. Please read the manual and set it in .env file.")
        exit(1)

    # Check if LLM API is working
    llm_client = LLMClient()
    response = llm_client.prompt_for_greeting()
    if response:
        logger.info("LLM API is working.")
    else:
        logger.error("LLM API is not working.")
        exit(1)


def check_embedding_model():
    if not settings.VDB_MODEL:
        logger.error("VDB_MODEL is not set. Please set it in settings.py.")
        exit(1)

    model = SentenceTransformer(settings.VDB_MODEL)
    schema_embeddings = model.encode("test")
    if len(schema_embeddings) > 0:
        logger.info("Transformer model is working.")
    else:
        logger.error("Transformer model is not working.")
        exit(1)


def check_vector_db():
    # Check if VectorDB is working
    logger.info("Load schemas and embed into VDB...")
    sdb = SchemaDB()
    try:
        sdb.init_db()
        n_indices = sdb.index.ntotal
        if n_indices > 0:
            logger.info("VectorDB is working.")
        else:
            logger.warning("VectorDB index is empty.")
    except ValueError:
        logger.error("VectorDB is not working.")
        exit(1)


def check_trino_api():
    # Check Trino Databases
    if not settings.TRINO_DATABASES:
        logger.warning("TRINO_DATABASES is not set. Please set it in settings.py.")

    # Check if Trino API is working
    trinodb = TrinoDB()
    if trinodb.test_connection():
        logger.info("Trino API is working.")
    else:
        logger.warning("Trino API is not working.")
