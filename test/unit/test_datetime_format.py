import re
import pytest
from datetime import datetime
from src.utils.datetime_format import format_jira_date


JIRA_DATE_REGEX = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.000\+\d{4}$"
)

@pytest.mark.parametrize("dt", [
    datetime(2024, 1 ,2 ,3 ,4 ,5),
    datetime(2035, 12, 31, 23, 59, 59),
    datetime(9999, 1, 1, 0, 0, 0),
    datetime.now()
])
def test_format_jira_date_datetime_now(dt: datetime) -> None:
    result = format_jira_date(dt)
    assert JIRA_DATE_REGEX.fullmatch(result), f"Invalid result: {result}"