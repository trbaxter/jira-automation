import logging
import os

from src.logging_config.configure_logging import log_config
from src.auth.session import get_authenticated_session
from src.helpers.config_accessor import get_board_config
from src.orchestration.sprint_orchestration import automate_sprint

if __name__ == "__main__":
    log_config()

    try:
        board_key = os.environ.get("BOARD")
        if not board_key:
            raise ValueError("YAML board environment variable is not set.")

        config = get_board_config(board_key)
        session = get_authenticated_session()
        automate_sprint(board_key, session)

    except SystemExit as e:
        logging.error(f"Process terminated: {e}")
        raise
    except Exception as e:
        logging.exception("Unexpected error occurred.")
        raise
