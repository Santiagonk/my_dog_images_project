import psycopg2
import logging

from app.settings.settings import Settings


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatabaseConnection:    
    def __init__(self):
        self.db_config = {
            'dbname': Settings.POSTGRES_DB,
            'user': Settings.POSTGRES_USER,
            'password': Settings.POSTGRES_PASSWORD,
            'host': Settings.POSTGRES_HOST,
            'port': Settings.POSTGRES_PORT
        }

    def create_connection(self):
        """Crea una conexión a la base de datos PostgreSQL."""
        try:
            conn = psycopg2.connect(**self.db_config)
            logger.info("Conexión a la base de datos establecida.")
            return conn
        except psycopg2.Error as e:
            logger.error(f"Error al conectar a la base de datos: {e}")
            raise

    def close_connection(self, conn):
        """Cierra la conexión a la base de datos."""
        if conn:
            conn.close()
            logger.info("Conexión a la base de datos cerrada.")
