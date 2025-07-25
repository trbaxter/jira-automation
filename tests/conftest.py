import logging

import pytest


@pytest.fixture(autouse=True)
def reset_root_handlers():
    root = logging.getLogger()
    root.handlers.clear()
    root.setLevel(logging.NOTSET)
