from unittest.mock import patch, mock_open

import pytest
from pydantic import HttpUrl

from src.exceptions.config_not_found_error import ConfigNotFoundError
from src.models.board_config import BoardConfig
from src.utils.config_loader import load_config

_VALID_YAML = (
    """
    board_id: 123
    base_url: "https://example.com/"
    board_name: "Some Test Board"
    """
)


# Valid file should return a valid BoardConfig object with valid attributes
def test_load_config_success() -> None:
    with patch("pathlib.Path.open", mock_open(read_data=_VALID_YAML)):
        result = load_config()
        assert isinstance(result, BoardConfig)
        assert result.board_id == 123
        assert result.base_url == HttpUrl("https://example.com/")
        assert result.board_name == "Some Test Board"


# ConfigNotFoundError should be raised if config file absent
def test_load_config_missing_yaml() -> None:
    with patch("pathlib.Path.open", side_effect=FileNotFoundError):
        with pytest.raises(ConfigNotFoundError):
            load_config()


# Using a non-dictionary mapping yaml config should raise TypeError
def test_load_config_malformed_yaml() -> None:
    with patch("pathlib.Path.open", mock_open(read_data="abc123")):
        with pytest.raises(TypeError):
            load_config()
