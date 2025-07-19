import logging

def log_config(level: int = logging.INFO) -> None:
    """
    Sets up the root logger using a message-only format.

    Configures Python's root logger to use the specified logging level and
    a minimal formatter that outputs only the message text, as the repository
    workflow action that the logs will display in already contain timestamps.

    Args:
        level: Logging level to set. Can use 'logging.INFO', 'logging.DEBUG',
               or 'logging.ERROR'. Defaults to 'logging.INFO'.

    Returns:
        None
    """
    logging.basicConfig(
        level=level,
        format="%(message)s",
        force=True
    )