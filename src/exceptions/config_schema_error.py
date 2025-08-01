class ConfigSchemaError(Exception):
    """
    Raised when the configuration file exists but its structure is invalid
    or required fields are missing.
    """

    def __init__(self, details: str) -> None:
        msg = f"Invalid configuration in board_config.yaml schema. {details}"
        super().__init__(msg)
