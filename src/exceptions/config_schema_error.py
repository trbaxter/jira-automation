class ConfigSchemaError(Exception):
    """
    Raised when the configuration file exists but its structure is invalid
    or required fields are missing.
    """

    def __init__(self, details: str) -> None:
        msg = "Invalid configuration in board_config.yaml schema. %s" % details
        super().__init__(msg)
