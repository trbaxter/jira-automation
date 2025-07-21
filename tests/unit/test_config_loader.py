from unittest.mock import mock_open, patch

import pytest

from src.utils.config_loader import load_config
from src.type_defs.boardconfig import BoardConfig

VALID_CONFIG_YAML = """
boards:
    test:
        id: 4
        base_url: "https://test123.atlassian.net/"
        name: "Some Fake Scrum Board"
"""

MISSING_BOARDS_YAML = """
not_boards_attribute:
    some_other_thing: true
"""

REAL_PATH = "board_config.yaml"
TEST_PATH = "some_dummy_path.yaml"


class TestLoadConfig:
    def test_loads_valid_config_with_mock(self) -> None:
        with (patch("pathlib.Path.open",
                    mock_open(read_data=VALID_CONFIG_YAML)),
              patch("pathlib.Path.exists", return_value=True)):
            result = load_config(TEST_PATH)
            assert isinstance(result, dict)
            assert "test" in result

            board: BoardConfig = result["test"]
            assert board["id"] == 4
            assert board["base_url"] == "https://test123.atlassian.net/"
            assert board["name"] == "Some Fake Scrum Board"

    def test_raises_key_error_on_missing_boards(self) -> None:
        with (patch("pathlib.Path.open",
                    mock_open(read_data=MISSING_BOARDS_YAML)),
              patch("pathlib.Path.exists", return_value=True)):
            with pytest.raises(
                    KeyError,
                    match="Required section 'boards' missing"):
                load_config(TEST_PATH)

    def test_raises_file_not_found_on_missing_file(self) -> None:
        with patch("pathlib.Path.exists", return_value=False):
            with pytest.raises(FileNotFoundError,
                               match="board_config.yaml not found"):
                load_config(TEST_PATH)
