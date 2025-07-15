import logging
import io
import pytest
from contextlib import redirect_stdout

from logging_config.logging_config import configure_logger


def test_configure_logger_outputs_to_console() -> None:
    # Create empty, fake memory file to read log output
    log_output = io.StringIO()

    # Redirect stdout terminal output to be captured by log_output instead in this block
    with redirect_stdout(log_output):
        logger = configure_logger("test_logger", level = logging.INFO)
        logger.info("This is a test log message.")

    output = log_output.getvalue()
    assert "This is a test log message." in output


# Parameterize some bad input types to check against several at once
@pytest.mark.parametrize("invalid_name", [42, True, None, [], {}, object])
def test_logger_name_must_be_string(invalid_name) -> None:
    with pytest.raises(TypeError, match="Logger name must be a string."):
        configure_logger(invalid_name, level = logging.INFO)
