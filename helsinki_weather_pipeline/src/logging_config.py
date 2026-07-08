import logging
from logging.handlers import RotatingFileHandler


def setup_logging(level=logging.INFO):
    if logging.getLogger().handlers:
        return
    logging.basicConfig(
        level=level,
        format="%(name)s - %(levelname)s - %(message)s",
        handlers=[RotatingFileHandler("weather_app.log", maxBytes=1_000_000, backupCount=3)]
    )
