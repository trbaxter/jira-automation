import pytest
from hypothesis import given

from src.exceptions.jira_board_not_found_error import JiraBoardNotFoundError
from tests.strategies.common import cleaned_string


@given(board_name=cleaned_string())
def test_jira_board_not_found_raises_with_message(board_name: str) -> None:
    expected_msg = f"No board configuration found with name: {board_name}"

    with pytest.raises(JiraBoardNotFoundError) as error:
        raise JiraBoardNotFoundError(board_name=board_name)

    assert isinstance(error.value, JiraBoardNotFoundError)
    assert isinstance(error.value, Exception)

    assert error.value.args[0] == expected_msg
