import logging

from src.auth.session import get_authenticated_session
from src.logging_config.configure_logging import log_config
from src.orchestration.sprint_orchestration import automate_sprint
from src.utils.config_loader import load_config

if __name__ == "__main__":
    log_config()

    try:
        config = load_config()
        session = get_authenticated_session()
        automate_sprint(session)

    except SystemExit as e:
        logging.error(f"Process terminated: {e}")
        raise

    except Exception as e:
        logging.exception("Unexpected error occurred.")
        raise
