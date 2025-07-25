from pathlib import Path

import yaml
from pydantic import ValidationError

from exceptions.config_not_found_error import ConfigNotFoundError
from exceptions.config_schema_error import ConfigSchemaError
from src.models.board_config import BoardConfig

_CONFIG_PATH = Path(__file__).resolve().parents[2] / "board_config.yaml"


def load_config() -> BoardConfig:
    """
    Loads and validates JIRA board configurations.

    Returns:
        A dictionary mapping board aliases to their config details.

    Raises:
        FileNotFoundError: If the yaml config file is missing.
        KeyError: If the required 'boards' section is missing in the YAML file.
    """
    try:
        with _CONFIG_PATH.open("r", encoding="utf-8") as file:
            config = yaml.safe_load(file)
    except yaml.YAMLError as error:
        raise ConfigSchemaError(f"Invalid YAML syntax: {error}")


    if not _CONFIG_PATH.exists():
        raise ConfigNotFoundError()

    try:
        return BoardConfig(**config)
    except ValidationError as error:
        raise ConfigSchemaError(str(error))
