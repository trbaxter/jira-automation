from pathlib import Path

import yaml
from pydantic import ValidationError

from src.exceptions.config_error import ConfigError
from src.models.board_config import BoardConfig

filename = "board_config.yaml"


def load_config() -> BoardConfig:
    config_path = Path(__file__).resolve().parents[2] / filename

    """
    Loads and validates JIRA board configurations.

    Returns:
        A BoardConfig object containing configuration details.

    Raises:
        ConfigError: If the config file is missing or invalid in
                     structure or content.
    """
    try:
        with config_path.open(mode="r", encoding="utf-8") as file:
            config = yaml.safe_load(file)

            if config is None:
                raise ConfigError(
                    "Expected a non-empty configuration for "
                    f"'{filename}'.")

            if not isinstance(config, dict):
                raise ConfigError(
                    f"Invalid file structure in '{filename}'."
                )

            return BoardConfig(**config)

    except FileNotFoundError:
        raise ConfigError.file_not_found()
    except ValidationError as e:
        raise ConfigError.from_validation_error(e)
