import re
from datetime import datetime

from hypothesis import given

from src.utils.datetime_format import format_jira_date
from tests.strategies.shared import valid_datetime_range

JIRA_DATE_REGEX = re.compile(
    r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.000\+\d{4}$'
)


@given(valid_datetime_range())
def test_format_jira_date_success(dt: datetime) -> None:
    result = format_jira_date(dt)
    assert JIRA_DATE_REGEX.fullmatch(result)
