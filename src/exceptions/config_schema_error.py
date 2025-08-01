from __future__ import annotations

from pydantic import ValidationError


class ConfigSchemaError(Exception):
    """
    Raised when the configuration file exists but its structure is invalid
    or required fields are missing.
    """

    def __init__(self, detail: str) -> None:
        msg = f"Invalid configuration in board_config.yaml: {detail}"
        super().__init__(msg)

    @staticmethod
    def from_validation_error(e: ValidationError) -> ConfigSchemaError:
        return ConfigSchemaError(str(e))