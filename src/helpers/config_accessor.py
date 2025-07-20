from src.utils.config_loader import BoardConfig
from src.utils.config_loader import load_config


def get_board_config(
        board_name: str,
        path: str = "board_config.yaml"
) -> BoardConfig:
    """
    Retrieves the configuration for a specified JIRA board.

    Args:
        board_name: The alias of the board to retrieve.
        path: Optional path to the YAML configuration file.

    Returns:
        The configuration dictionary for the specified board.

    Raises:
        KeyError: If the specified board alias does not exist.
    """
    config = load_config(path)
    if board_name not in config:
        raise KeyError(f"Board name '{board_name}' not found in {path}.")
    return config[board_name]