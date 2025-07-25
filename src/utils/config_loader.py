from pathlib import Path
from typing import Dict

import yaml

from src.models.boardconfig import BoardConfig


def load_config(path: str = "board_config.yaml") -> Dict[str, BoardConfig]:
    """
    Loads and validates JIRA board configurations.

    Args:
        path: Optional path to the YAML configuration file. Defaults to
              'board_config.yaml' in the root directory.

    Returns:
        A dictionary mapping board aliases to their config details.

    Raises:
        FileNotFoundError: If the yaml config file is missing.
        KeyError: If the required 'boards' section is missing in the YAML file.
    """
    full_path = Path(path)
    if not full_path.exists():
        raise FileNotFoundError(
            f"board_config.yaml not found in root directory."
        )

    with full_path.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    if "boards" not in config:
        raise KeyError(
            "Required section 'boards' missing in board_config.yaml."
        )

    return config["boards"]
