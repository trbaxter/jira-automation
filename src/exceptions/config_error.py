from __future__ import annotations

from pydantic import ValidationError


class ConfigError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)

    @classmethod
    def file_not_found(cls) -> ConfigError:
        return cls(
            'Configuration error: '
            'Missing board_config.yaml configuration file in project root.'
        )

    @classmethod
    def from_validation_error(cls, e: ValidationError) -> ConfigError:
        missing_fields = [
            '.'.join(str(loc) for loc in err['loc'])
            for err in e.errors()
            if err['type'] in {'missing', 'value_error.missing'}
        ]

        if not missing_fields:
            return cls(f'Configuration error: {str(e)}')

        if len(missing_fields) == 1:
            return cls(
                f'Missing key in board_config.yaml: {missing_fields[0]}'
            )

        keys = ', '.join(missing_fields)
        return cls(f'Missing keys in board_config.yaml: {keys}')