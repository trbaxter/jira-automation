import logging

from src.constants.field_types import INT_GEQ_0


def log_config(level: INT_GEQ_0 = logging.INFO, force: bool = True) -> None:
    """
    Sets up the root logger using a message-only format.

    Configures Python's root logger to use the specified logging level and
    a minimal formatter that outputs only the message text, as the repository
    workflow action that the logs will display in already contain timestamps.

    Args:
        level: Logging level to set.
        force: Forces removal of previously attached logging handlers if True.
    """
    logging.basicConfig(level=level, format="%(message)s", force=force)
