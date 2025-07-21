import logging
import os

from src.auth.session import get_authenticated_session
from src.orchestration.sprint_orchestration import automate_sprint
from src.helpers.config_accessor import get_board_config

if __name__ == "__main__":
    try:
        board_name = os.environ.get("BOARD")
        if not board_name:
            raise ValueError("BOARD environment variable is not set.")

        config = get_board_config(board_name=board_name)
        session = get_authenticated_session()

        automate_sprint(board_name=board_name, session=session)

    except SystemExit as e:
        logging.error(f"Process terminated: {e}")
        raise
    except Exception as e:
        logging.exception("Unexpected error occurred.")
        raise
