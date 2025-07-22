from src.helpers.payload_builder import build_close_sprint_payload
from tests.constants.test_constants import (
    CLOSED,
    MOCK_SPRINT_END,
    MOCK_SPRINT_NAME,
    MOCK_SPRINT_START
)

def test_build_close_sprint_payload_returns_expected_dict() -> None:
    result = build_close_sprint_payload(
        MOCK_SPRINT_NAME,
        MOCK_SPRINT_START,
        MOCK_SPRINT_END
    )

    expected = {
        "state": CLOSED,
        "name": MOCK_SPRINT_NAME,
        "startDate": MOCK_SPRINT_START,
        "endDate": MOCK_SPRINT_END
    }

    assert result == expected
