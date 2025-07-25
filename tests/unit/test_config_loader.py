from unittest.mock import mock_open, patch

import pytest

from src.models.boardconfig import BoardConfig
from src.utils.config_loader import load_config
from tests.constants.test_constants import TEST_YAML_PATH
from tests.constants.test_objects import (
    MISSING_BOARDS_YAML,
    VALID_CONFIG_YAML
)


class TestLoadConfig:
    def test_loads_valid_config_with_mock(self) -> None:
        with (
            patch("pathlib.Path.open", mock_open(read_data=VALID_CONFIG_YAML)),
            patch("pathlib.Path.exists", return_value=True)
        ):
            result = load_config(TEST_YAML_PATH)
            assert isinstance(result, dict)
            assert "test" in result

            board: BoardConfig = result["test"]
            assert board["board_id"] == 4
            assert board["base_url"] == "https://test123.atlassian.net/"
            assert board["board_name"] == "Some Fake Scrum Board"

    def test_raises_key_error_on_missing_boards(self) -> None:
        with (
            patch(
                "pathlib.Path.open",
                mock_open(read_data=MISSING_BOARDS_YAML)),
            patch("pathlib.Path.exists", return_value=True)
        ):
            with pytest.raises(
                    KeyError,
                    match="Required section 'boards' missing"
            ):
                load_config(TEST_YAML_PATH)

    def test_raises_file_not_found_on_missing_file(self) -> None:
        with patch("pathlib.Path.exists", return_value=False):
            with pytest.raises(
                    FileNotFoundError,
                    match="board_config.yaml not found"
            ):
                load_config(TEST_YAML_PATH)
