import re
from datetime import datetime, timedelta

from hypothesis import given

from src.models.sprint_close_payload import CloseSprintPayload
from src.models.sprint_start_payload import StartSprintPayload
from src.utils.datetime_format import format_jira_date
from src.utils.payload_builder import (
    build_close_sprint_payload,
    build_start_sprint_payload,
)
from tests.strategies.common import cleaned_string, valid_datetime_range

JIRA_DATE_REGEX = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.000\+\d{4}")


@given(sprint_name=cleaned_string(), start_date=valid_datetime_range())
def test_build_close_sprint_payload_success(
        sprint_name: str, start_date: datetime
) -> None:
    end_date = start_date + timedelta(days=14)

    start_str = format_jira_date(dt=start_date)
    end_str = format_jira_date(dt=end_date)

    payload = build_close_sprint_payload(
        sprint_name=sprint_name, start_date=start_str, end_date=end_str
    )

    assert isinstance(payload, CloseSprintPayload)

    assert payload.state == "closed"
    assert payload.name == sprint_name
    assert payload.startDate == start_str
    assert payload.endDate == end_str
    assert JIRA_DATE_REGEX.fullmatch(string=payload.startDate)
    assert JIRA_DATE_REGEX.fullmatch(string=payload.endDate)


@given(sprint_name=cleaned_string(), start_date=valid_datetime_range())
def test_build_start_sprint_payload(
        sprint_name: str,
        start_date: datetime,
) -> None:
    end_date = start_date + timedelta(days=14)

    payload = build_start_sprint_payload(
        sprint_name=sprint_name, start_date=start_date, end_date=end_date
    )

    assert isinstance(payload, StartSprintPayload)

    assert payload.state == "active"
    assert payload.name == sprint_name
    assert payload.startDate == format_jira_date(dt=start_date)
    assert payload.endDate == format_jira_date(dt=end_date)
