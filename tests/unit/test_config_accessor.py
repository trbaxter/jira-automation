from unittest.mock import patch

import pytest

from src.helpers.config_accessor import get_board_config
from src.utils.config_loader import BoardConfig
from tests.constants.patch_targets import CONFIG_ACCESS_LOAD_CONFIG
from tests.constants.test_constants import (
    DEV_BASE_URL,
    DEV_BOARD_NAME,
    QA_BASE_URL,
    QA_BOARD_NAME
)

MOCKED_CONFIG = {
    "dev": {
        "board_id": 123,
        "base_url": DEV_BASE_URL,
        "board_name": DEV_BOARD_NAME
    },
    "qa": {
        "board_id": 456,
        "base_url": QA_BASE_URL,
        "board_name": QA_BOARD_NAME
    }
}


class TestGetBoardConfig:

    @patch(CONFIG_ACCESS_LOAD_CONFIG, return_value=MOCKED_CONFIG)
    def test_returns_correct_board_config(self, mock_loader) -> None:
        board: BoardConfig = get_board_config("dev")
        assert board["board_id"] == 123
        assert board["base_url"] == DEV_BASE_URL
        assert board["board_name"] == DEV_BOARD_NAME

        mock_loader.assert_called_once()

    @patch(CONFIG_ACCESS_LOAD_CONFIG, return_value=MOCKED_CONFIG)
    def test_raises_key_error_for_unknown_alias(self, _mock_loader) -> None:
        with pytest.raises(KeyError, match="Board name 'uat' not found"):
            get_board_config("uat")
