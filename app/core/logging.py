import logging
import sys
from app.config import settings


def setup_logging():
    """Setup application logging"""
    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("logs/app.log", mode="a"),
        ],
    )
    # Suppress some verbose loggers
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    # cache_logger = logging.getLogger("app.services.cache_service")
    # cache_logger.setLevel(logging.INFO)
