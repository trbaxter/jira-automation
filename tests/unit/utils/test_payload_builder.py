import re
from datetime import datetime, timedelta

from hypothesis import given

from src.constants.shared import SAFE_STR
from src.models.sprint_close_payload import CloseSprintPayload
from src.models.sprint_start_payload import StartSprintPayload
from src.utils.datetime_format import format_jira_date
from src.utils.payload_builder import (
    build_close_sprint_payload,
    build_start_sprint_payload,
)
from tests.strategies.shared import cleaned_string, valid_datetime_range

JIRA_DATE_REGEX = re.compile(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.000\+\d{4}')


@given(cleaned_string(), valid_datetime_range())
def test_build_close_sprint_payload_success(
    sprint_name: SAFE_STR, start_date: datetime
) -> None:
    end_date = start_date + timedelta(days=14)

    start_str = format_jira_date(start_date)
    end_str = format_jira_date(end_date)

    payload = build_close_sprint_payload(sprint_name, start_str, end_str)

    assert isinstance(payload, CloseSprintPayload)

    assert payload.state == 'closed'
    assert payload.name == sprint_name
    assert payload.startDate == start_str
    assert payload.endDate == end_str
    assert JIRA_DATE_REGEX.fullmatch(payload.startDate)
    assert JIRA_DATE_REGEX.fullmatch(payload.endDate)


@given(cleaned_string(), valid_datetime_range())
def test_build_start_sprint_payload(
    sprint_name: SAFE_STR, start_date: datetime
) -> None:
    end_date = start_date + timedelta(days=14)

    payload = build_start_sprint_payload(sprint_name, start_date, end_date)

    assert isinstance(payload, StartSprintPayload)
    assert payload.state == 'active'
    assert payload.name == sprint_name
    assert payload.startDate == format_jira_date(start_date)
    assert payload.endDate == format_jira_date(end_date)
