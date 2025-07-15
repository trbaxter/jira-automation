import logging
import sys

def configure_logger(name: str, level = logging.INFO) -> logging.Logger:
    if not isinstance(name, str):
         raise TypeError(f"Logger name must be a string, got {type(name).__name__} instead.")

    logger = logging.getLogger(name)
    logger.setLevel(level)

    handler = logging.StreamHandler(sys.stdout)
    logger.addHandler(handler)

    return logger