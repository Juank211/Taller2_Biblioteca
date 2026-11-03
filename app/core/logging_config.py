import logging
import sys
from logging.handlers import StreamHandler

def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    console_handler = StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    # Configurar logging para SQLAlchemy y FastAPI
    logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
    logging.getLogger("uvicorn.error").setLevel(logging.INFO)
