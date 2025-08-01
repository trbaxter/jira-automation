from __future__ import annotations

from pydantic import ValidationError


class ConfigError(Exception):
    """
    Raised when the board_config.yaml file is missing or contains
    invalid structure or content.
    """

    def __init__(self, detail: str) -> None:
        msg = f"Configuration error detected. {detail}"
        super().__init__(msg)

    @staticmethod
    def file_not_found() -> ConfigError:
        return ConfigError(
            "Missing 'board_config.yaml' configuration file in project root."
        )

    @staticmethod
    def from_validation_error(e: ValidationError) -> ConfigError:
        return ConfigError(str(e))