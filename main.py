import logging
import sys

from src.auth.session import get_authenticated_session
from src.exceptions.config_not_found_error import ConfigNotFoundError
from src.logs.configure_logging import log_config
from src.orchestration.sprint_orchestration import automate_sprint
from src.utils.config_loader import load_config

if __name__ == "__main__":
    log_config()

    try:
        config = load_config()

    except ConfigNotFoundError as error:
        print(f"\nError: board_config.yaml missing in root directory\n")
        sys.exit(1)

    try:
        session = get_authenticated_session()
        automate_sprint(session, config)

    except Exception as e:
        logging.exception("An unexpected error occurred")
        raise
