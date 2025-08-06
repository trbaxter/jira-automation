import logging


def log_config(level: int = logging.INFO, force: bool = True) -> None:
    logging.basicConfig(level=level, format='%(message)s', force=force)
