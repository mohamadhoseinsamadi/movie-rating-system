import logging
import sys


def setup_logging():
    """
    Configure the logging system for the application.
    Sets up a StreamHandler to output logs to the console with a specific format.
    Format: TIMESTAMP - MODULE - LEVEL - MESSAGE
    """
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )

    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy").setLevel(logging.WARNING)
