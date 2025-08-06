import pytest
from pydantic import ValidationError

from src.exceptions.config_error import ConfigError
from src.models.board_config import BoardConfig


def test_file_not_found_message() -> None:
    error = ConfigError.file_not_found()
    assert 'Missing board_config.yaml configuration file' in str(error)


def test_from_validation_error_single_missing_field() -> None:
    incomplete_config = {
        'base_url': 'https://example.net',
        'board_id': 123
        # no board_name
    }

    with pytest.raises(ValidationError) as exception:
        BoardConfig(**incomplete_config)

    err = ConfigError.from_validation_error(exception.value)
    assert 'Missing key in board_config.yaml: board_name' in str(err)



def test_from_validation_error_two_missing_fields() -> None:
    incomplete_config = {
        'base_url': 'https://example.net',
        # no board_id
        # no board_name
    }

    with pytest.raises(ValidationError) as exception:
        BoardConfig(**incomplete_config)

    err = ConfigError.from_validation_error(exception.value)
    assert (
        'Missing keys in board_config.yaml:'
        and 'board_id' and 'board_name' in str(err)
    )


def test_from_validation_error_all_fields_missing() -> None:
    incomplete_config = {
        # no base_url
        # no board_id
        # no board_name
    }

    with pytest.raises(ValidationError) as exception:
        BoardConfig(**incomplete_config)

    err = ConfigError.from_validation_error(exception.value)
    assert (
        'Missing keys in board_config.yaml:'
        and 'base_url' and 'board_id' and 'board_name' in str(err)
    )


def test_from_validation_error_non_missing_type() -> None:
    invalid_config = {
        'base_url': 'https://example.net',
        'board_id': 123,
        'board_name': 456
    }

    with pytest.raises(ValidationError) as exception:
        BoardConfig(**invalid_config)

    err = ConfigError.from_validation_error(exception.value)
    assert (
            'Configuration error' in str(err)
    )

