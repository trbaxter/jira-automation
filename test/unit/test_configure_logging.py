import logging
from _pytest.logging import LogCaptureFixture
from src.logging_config.configure_logging import log_config


# Used to prevent log results from appearing in pytest output
logging.getLogger().handlers.clear()


def test_configure_logging_sets_level() -> None:
    log_config(logging.DEBUG)
    logger = logging.getLogger()
    assert logger.getEffectiveLevel() == logging.DEBUG



def test_configure_logging_sets_format(caplog: LogCaptureFixture) -> None:
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    with caplog.at_level(logging.INFO):
        logger.info("Hello world")

    assert "Hello world" in caplog.text