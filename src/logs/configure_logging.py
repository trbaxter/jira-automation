import logging

from src.customtypes.shared import PositiveInt


def log_config(level: PositiveInt = logging.INFO, force: bool = True) -> None:
    logging.basicConfig(level=level, format='%(message)s', force=force)
