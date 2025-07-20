import yaml
from pathlib import Path
from typing import Dict, TypedDict


class BoardConfig(TypedDict):
    id: int
    base_url: str
    name: str


def load_config(path: str = "board_config.yaml") -> Dict[str, BoardConfig]:
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