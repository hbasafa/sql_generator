import faiss
import numpy as np
from src.app import settings
from src.logging.log_manager import logger
from src.database import db_manager
from sentence_transformers import SentenceTransformer


# TODO: Make sure a good vector similarity function is chosen


class SchemaDB:
    def __init__(self):
        self.model = SentenceTransformer(settings.VDB_MODEL)
        self.index = faiss.IndexFlatL2(self.model.get_sentence_embedding_dimension())

        self.schema_context = []
        self.schema_embeddings = []
        self.top_k = settings.VDB_TOP_K

    def set_schema_context(self, schemas):
        self.schema_context = schemas

    def get_schemas(self):
        return db_manager.get_schema()

    def get_schema_embeddings(self, schemas):
        if not schemas:
            logger.warning("Schema context is empty.")
        return self.model.encode(schemas)

    def add_index(self, embeddings):
        if embeddings is None or len(embeddings) == 0:
            logger.warning("Embeddings is empty.")
        self.index.add(np.array(embeddings))

    def search(self, query_embedding):
        try:
            return self.index.search(np.array(query_embedding), self.top_k)
        except ValueError as e:
            logger.error(f"Error in searching the database: {e}")
            raise e

    def init_db(self):
        self.schema_context = self.get_schemas()
        self.schema_embeddings = self.get_schema_embeddings(self.schema_context)
        self.add_index(self.schema_embeddings)

    def retrieve_relevant_schema(self, user_query):
        logger.info("Retrieving relevant schema...")
        query_embedding = self.model.encode([user_query])
        distances, indices = self.search(query_embedding)
        relevant_schema = [self.schema_context[idx] for idx in indices[0]]
        return relevant_schema
