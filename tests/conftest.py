import logging

import pytest

from tests.constants.patch_targets import (BOARD_CONFIG, JSPRINT_GET_CONFIG)
from tests.constants.test_constants import (
    MOCK_BASE_URL,
    MOCK_BOARD_NAME,
    YAML_CONFIG_PATH
)


@pytest.fixture(autouse=True)
def reset_root_handlers():
    root = logging.getLogger()
    root.handlers.clear()
    root.setLevel(logging.NOTSET)


@pytest.fixture(autouse=True)
def patch_get_board_config(monkeypatch):
    from src.helpers.config_accessor import BoardConfig

    def _mock_get_board_config(
            board_name: str,
            path: str = YAML_CONFIG_PATH
    ) -> BoardConfig:
        _ = board_name, path  # Required in function, but not used
        return {
            "board_id": 1,
            "base_url": MOCK_BASE_URL,
            "board_name": MOCK_BOARD_NAME
        }

    monkeypatch.setattr(BOARD_CONFIG, _mock_get_board_config)
    monkeypatch.setattr(JSPRINT_GET_CONFIG, _mock_get_board_config)
