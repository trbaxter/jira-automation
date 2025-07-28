from datetime import datetime

import pytest
from hypothesis import given
from pydantic import ValidationError

from models.sprint_payload import SprintPayload
from strategies.common import cleaned_string, valid_datetime_range

VALID_INPUT = {
    "name": "Sprint 12345",
    "startDate": "2024-12-25T12:00:00.000+0000",
    "endDate": "2025-01-08T12:00:00.000+0000",
    "originBoardId": 100,
}


def test_valid_static_input() -> None:
    payload = SprintPayload(**VALID_INPUT)
    assert isinstance(payload, SprintPayload)
    assert payload.model_dump() == VALID_INPUT


@given(name=cleaned_string())
def test_valid_varied_name(name: str) -> None:
    data = {**VALID_INPUT, "name": name}
    payload = SprintPayload(**data)
    assert isinstance(payload, SprintPayload)


@pytest.mark.parametrize("bad_date", ["2024-01-01", "", "not-a-date"])
def test_bad_date_inputs(bad_date: str) -> None:
    with pytest.raises(expected_exception=ValidationError):
        data = {**VALID_INPUT, "startDate": bad_date}
        SprintPayload(**data)


@given(dt=valid_datetime_range())
def test_pydantic_rejects_non_formatted_datetimes(dt: datetime) -> None:
    with pytest.raises(expected_exception=ValidationError):
        data = {**VALID_INPUT, "startDate": dt, "endDate": dt}
        SprintPayload(**data)
