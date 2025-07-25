import logging

from _pytest.logging import LogCaptureFixture

from src.logging_config.configure_logging import log_config


def test_configure_logging_sets_level() -> None:
    log_config(logging.DEBUG)
    logger = logging.getLogger()
    assert logger.getEffectiveLevel() == logging.DEBUG


def test_configure_logging_sets_format(caplog: LogCaptureFixture) -> None:
    log_config(logging.INFO, force=False)
    logger = logging.getLogger()

    with caplog.at_level(logging.INFO):
        logger.info("Hello world")

    assert "Hello world" in caplog.text
