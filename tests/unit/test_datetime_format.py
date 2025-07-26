import re
from datetime import datetime

from hypothesis import given, settings
from hypothesis.strategies import datetimes

from src.utils.datetime_format import format_jira_date

JIRA_DATE_REGEX = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.000\+\d{4}$"
)


@given(dt=datetimes(min_value=datetime(2025, 1, 1)))
@settings(max_examples=5000)
def test_format_jira_date_success(dt: datetime) -> None:
    result = format_jira_date(dt)
    assert JIRA_DATE_REGEX.fullmatch(result)
