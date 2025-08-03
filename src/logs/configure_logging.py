import logging

from src.constants.shared import INT_GEQ_0


def log_config(level: INT_GEQ_0 = logging.INFO, force: bool = True) -> None:
    logging.basicConfig(level=level, format="%(message)s", force=force)
