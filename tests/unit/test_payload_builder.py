import re
from datetime import datetime, timedelta

from hypothesis import assume, given, settings
from hypothesis.strategies import text, datetimes

from src.utils.datetime_format import format_jira_date
from src.utils.payload_builder import build_close_sprint_payload

JIRA_DATE_REGEX = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.000\+\d{4}")


@given(
    name=text(min_size=1),
    start_dt=datetimes(min_value=datetime(2025, 1, 1))
)
@settings(max_examples=5000)
def test_build_close_sprint_payload_returns_expected_dict(
        name: str,
        start_dt: datetime
) -> None:
    assume(start_dt.year >= 2025)
    end_dt = start_dt + timedelta(days=13)

    start_str = format_jira_date(start_dt)
    end_str = format_jira_date(end_dt)

    result = build_close_sprint_payload(name, start_str, end_str)

    assert result["state"] == "closed"
    assert result["name"] == name
    assert result["startDate"] == start_str
    assert result["endDate"] == end_str
    assert JIRA_DATE_REGEX.fullmatch(result["startDate"])
    assert JIRA_DATE_REGEX.fullmatch(result["endDate"])
