import logging
import sys

from src.auth.session import get_authenticated_session
from src.exceptions.config_error import ConfigError
from src.logs.configure_logging import log_config
from src.orchestration.sprint_orchestration import automate_sprint
from src.utils.config_loader import load_config

if __name__ == '__main__':
    log_config()

    try:
        config = load_config()
    except ConfigError as e:
        print(f'Error: {e}')
        sys.exit(1)

    try:
        session = get_authenticated_session()
        automate_sprint(session, config)

    except Exception as e:
        logging.exception('An unexpected error occurred')
        raise
