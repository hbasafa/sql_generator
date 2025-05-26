from src.app import settings
import logging
import logging.config

logging.config.dictConfig(settings.LOGGING_CONFIG)
logger = logging.getLogger(settings.DEFAULT_LOGGER)
logger.info('Logger initialized.')
