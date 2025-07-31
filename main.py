import logging
import sys

from src.auth.session import get_authenticated_session
from src.constants.shared import BOLD_RED, TEXT_RESET
from src.exceptions.config_not_found_error import ConfigNotFoundError
from src.logs.configure_logging import log_config
from src.orchestration.sprint_orchestration import automate_sprint
from src.utils.config_loader import load_config

if __name__ == "__main__":
    log_config()

    try:
        config = load_config()

    except ConfigNotFoundError as error:
        print(
            f"{BOLD_RED}[ERROR]: "
            f"board_config.yaml missing in root directory{TEXT_RESET}"
        )
        sys.exit(1)

    try:
        session = get_authenticated_session()
        automate_sprint(session)

    except Exception as e:
        logging.exception("Unexpected error occurred")
        raise
