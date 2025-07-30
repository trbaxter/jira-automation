from pathlib import Path

import yaml

from src.exceptions.config_not_found_error import ConfigNotFoundError
from src.models.board_config import BoardConfig

CONFIG_PATH = Path(__file__).resolve().parents[2] / "board_config.yaml"


def load_config() -> BoardConfig:
    """
    Loads and validates JIRA board configurations.

    Returns:
        A BoardConfig object containing configuration details.

    Raises:
        TypeError: If the yaml doesn't use the proper dict format.
        FileNotFoundError: If the yaml config file is missing.
    """
    try:
        with CONFIG_PATH.open(mode="r", encoding="utf-8") as file:
            config = yaml.safe_load(file)

            if not isinstance(config, dict):
                raise TypeError("YAML content must be a dictionary mapping")

            return BoardConfig(**config)

    except FileNotFoundError:
        raise ConfigNotFoundError()
