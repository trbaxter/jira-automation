from pathlib import Path

import yaml
from pydantic import ValidationError

from src.exceptions.config_not_found_error import ConfigNotFoundError
from src.exceptions.config_schema_error import ConfigSchemaError
from src.models.board_config import BoardConfig


def load_config() -> BoardConfig:
    config_path = Path(__file__).resolve().parents[2] / "board_config.yaml"

    """
    Loads and validates JIRA board configurations.

    Returns:
        A BoardConfig object containing configuration details.

    Raises:
        TypeError: If the yaml doesn't use the proper dict format.
        FileNotFoundError: If the yaml config file is missing.
    """
    try:
        with config_path.open(mode="r", encoding="utf-8") as file:
            config = yaml.safe_load(file)
            if not isinstance(config, dict):
                raise ConfigSchemaError("Expected a top-level dictionary.")
            return BoardConfig(**config)
    except FileNotFoundError:
        raise ConfigNotFoundError()
    except ValidationError as e:
        raise ConfigSchemaError.from_validation_error(e)
