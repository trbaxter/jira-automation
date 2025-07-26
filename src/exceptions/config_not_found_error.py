class ConfigNotFoundError(FileNotFoundError):
    """
    Raised when the board_config.yaml file is missing from the expected
    location.
    """

    def __init__(self) -> None:
        msg = (
            "Expected configuration file 'board_config.yaml' not found "
            "in root directory."
        )
        super().__init__(msg)
