
from src.logging.log_manager import logger
from src.llm.sql_generator import SQLGenerator
from src.app.dto_models import QueryRequest, QueryResponse
from fastapi import FastAPI, HTTPException


class API:
    def __init__(self):

        logger.info("Initializing FastAPI app...")
        self.app = FastAPI(title="SQL Generator Service", version="1.0")
        self.sql_generator = SQLGenerator()

        self.app.add_api_route("/health", self.check_health, methods=["GET"])
        self.app.add_api_route("/generate_sql", self.generate_sql, methods=["POST"], response_model=QueryResponse)

    def generate_sql(self, request: QueryRequest):
        try:
            response = self.sql_generator.generate_sql_query(request.question)
            logger.debug(f"Response: {response}")
            return response
        except HTTPException as e:
            logger.error(e, exc_info=True)
            raise HTTPException(status_code=500, detail=f"LLM error: {e}")
        except TypeError as e:
            logger.error(e, exc_info=True)
            raise HTTPException(status_code=500, detail=f"Type error: {e}")
        except ValueError as e:
            logger.error(e, exc_info=True)
            raise HTTPException(status_code=500, detail=f"Invalid question: {e}")
        except Exception as e:
            logger.error(e, exc_info=True)
            raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")

    def check_health(self):
        return {"status": "ok", "message": "SQL Generator Service is running."}

    def get_app(self):
        return self.app
