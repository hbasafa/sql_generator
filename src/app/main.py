import uvicorn
from src.app import settings
from src.logging.log_manager import logger
from src.app import bootstrap
from src.app.api import API


def run_app():
    logger.info("Starting the FastAPI app via uvicorn...")
    uvicorn.run(API().get_app(), host=settings.APP_HOST, port=settings.APP_PORT, log_config=settings.LOGGING_CONFIG)


def main():
    logger.info("Starting SQL Generator Service...")

    # Initial checks
    bootstrap.init()

    # Run the app
    run_app()


if __name__ == "__main__":
    main()
