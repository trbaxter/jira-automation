import pytest
from pydantic import ValidationError

from src.models.sprint_create_response import SprintCreateResponse

ID = "id"
SELF = "self"
STATE = "state"
NAME = "name"
START = "startDate"
END = "endDate"
BOARD_ID = "originBoardId"

VALID_RESPONSE = {
    ID: 1,
    SELF: "https://jira.example.com/sprint/1",
    STATE: "active",
    NAME: "Sprint 42",
    START: "2024-11-01T00:00:00.000Z",
    END: "2024-11-14T23:59:59.000Z",
    BOARD_ID: 100,
}


def test_response_accepts_valid_data() -> None:
    result = SprintCreateResponse(**VALID_RESPONSE)

    for field, value in VALID_RESPONSE.items():
        assert getattr(result, field) == value


@pytest.mark.parametrize(
    "field, bad_value",
    [
        (ID, 0),
        (BOARD_ID, -1),
        (STATE, "   "),
        (NAME, ""),
    ],
)
def test_response_rejects_invalid_fields(
        field: str, bad_value: int | str
) -> None:
    invalid_data = VALID_RESPONSE.copy()
    invalid_data[field] = bad_value

    with pytest.raises(ValidationError) as error:
        SprintCreateResponse(**invalid_data)

    assert field in str(error.value)
