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
        A BoardConfig object containing configuration details.

    Raises:
        FileNotFoundError: If the yaml config file is missing.
        KeyError: If the required 'boards' section is missing in the YAML file.
    """
    try:
        with _CONFIG_PATH.open("r", encoding="utf-8") as file:
            config = yaml.safe_load(file)
            return BoardConfig(**config)

    except FileNotFoundError:
        raise ConfigNotFoundError()

    except yaml.YAMLError as error:
        err_msg = str(error).splitlines()[2].strip()
        formatted_error = err_msg[0].upper() + err_msg[1:]
        raise ConfigSchemaError(
            f"{formatted_error}"
        )

    except ValidationError as error:
        raise ConfigSchemaError(str(error))
