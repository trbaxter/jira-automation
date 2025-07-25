from pathlib import Path

import yaml

from exceptions.config_not_found_error import ConfigNotFoundError
from src.models.board_config import BoardConfig

_CONFIG_PATH = Path(__file__).resolve().parents[2] / "board_config.yaml"


def load_config() -> BoardConfig:
    """
    Loads and validates JIRA board configurations.

    Returns:
        A BoardConfig object containing configuration details.

    Raises:
        FileNotFoundError: If the yaml config file is missing.
    """
    try:
        with _CONFIG_PATH.open("r", encoding="utf-8") as file:
            config = yaml.safe_load(file)
            return BoardConfig(**config)

    except FileNotFoundError:
        raise ConfigNotFoundError()
