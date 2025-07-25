from src.exceptions.jira_board_not_found import JiraBoardNotFound
from src.utils.config_loader import BoardConfig, load_config


def get_board_config(board_name: str) -> BoardConfig:
    """
    Obtains a Jira board configuration based on board name.

    Args:
        board_name: Alias of the Jira board.

    Returns:
        Object containing 'board_id', 'base_url', and 'board_name'
        attributes from board_config.yaml.
    """
    config = load_config()
    try:
        return config[board_name]
    except KeyError:
        raise JiraBoardNotFound(board_name)
