class JiraBoardNotFoundError(KeyError):
    """
    Raised when a board configuration is requested using an undefined alias.
    """

    def __init__(self, board_name: str) -> None:
        msg = f"No board configuration found with name: {board_name}"
        super().__init__(msg)
