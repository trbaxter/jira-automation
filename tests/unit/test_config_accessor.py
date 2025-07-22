import pytest
from unittest.mock import patch
from src.helpers.config_accessor import get_board_config
from src.utils.config_loader import BoardConfig

DEV_URL = "https://dev.atlassian.net/"
DEV_NAME = "Dev Board"
QA_URL = "https://qa.atlassian.net/"
QA_NAME = "QA Board"
LOAD_CONFIG_PATH = "src.helpers.config_accessor.load_config"

MOCKED_CONFIG = {
    "dev": {
        "board_id": 123,
        "base_url": DEV_URL,
        "board_name": DEV_NAME
    },
    "qa": {
        "board_id": 456,
        "base_url": QA_URL,
        "board_name": QA_NAME
    }
}


class TestGetBoardConfig:

    @patch(LOAD_CONFIG_PATH, return_value=MOCKED_CONFIG)
    def test_returns_correct_board_config(self, mock_loader) -> None:
        board: BoardConfig = get_board_config("dev")
        assert board["board_id"] == 123
        assert board["base_url"] == DEV_URL
        assert board["board_name"] ==  DEV_NAME

        mock_loader.assert_called_once()

    @patch(LOAD_CONFIG_PATH, return_value=MOCKED_CONFIG)
    def test_raises_key_error_for_unknown_alias(self, _mock_loader) -> None:
        with pytest.raises(KeyError, match="Board name 'uat' not found"):
            get_board_config("uat")