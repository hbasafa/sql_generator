import trino
from src.app import settings
from src.logging.log_manager import logger


class TrinoDB:
    def __init__(self):
        self.connection = trino.dbapi.connect(
            host=settings.TRINO_HOST,
            port=settings.TRINO_PORT,
            user=settings.TRINO_USER,
        )

    def query_trino(self, sql: str):
        cursor = self.connection.cursor()
        cursor.execute(sql)
        return cursor.fetchall()

    def test_connection(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            if result[0] == 1:
                return True
            else:
                return False
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return False
