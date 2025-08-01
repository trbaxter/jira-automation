import pytest

from src.exceptions.config_schema_error import ConfigSchemaError


def test_config_schema_error_raises_with_message() -> None:
    details = "Missing required field: board_id"
    expected_msg = (
        f"Invalid configuration in board_config.yaml. {details}"
    )

    with pytest.raises(ConfigSchemaError) as error:
        raise ConfigSchemaError(details)

    error_type = error.value.__class__.__name__

    assert isinstance(error.value, ConfigSchemaError)
    assert isinstance(error.value, Exception)
    assert str(error.value) == expected_msg
    assert repr(error.value) == f"{error_type}('{expected_msg}')"
