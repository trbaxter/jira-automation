from pathlib import Path
from typing import Dict

import yaml

from src.models.boardconfig import BoardConfig

_CONFIG_PATH = Path(__file__).resolve().parents[2] / "board_config.yaml"


def load_config() -> Dict[str, BoardConfig]:
    """
    Loads and validates JIRA board configurations.

    Returns:
        A dictionary mapping board aliases to their config details.

    Raises:
        FileNotFoundError: If the yaml config file is missing.
        KeyError: If the required 'boards' section is missing in the YAML file.
    """
    if not _CONFIG_PATH.exists():
        raise FileNotFoundError(
            f"board_config.yaml not found in root directory."
        )

    with _CONFIG_PATH.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    if "boards" not in config:
        raise KeyError(
            "Required section 'boards' missing in board_config.yaml."
        )

    return config["boards"]
