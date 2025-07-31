import re
from datetime import datetime, timedelta

from hypothesis import given

from src.utils.sprint_naming import generate_sprint_name
from tests.strategies.shared import valid_datetime_range


@given(valid_datetime_range())
def test_sprint_name_generation(start_date: datetime) -> None:
    end_date = start_date + timedelta(days=14)
    result = generate_sprint_name(start_date, end_date)

    prefix = start_date.strftime("%y%m%d")
    start_fmt = start_date.strftime("%m/%d")
    end_fmt = end_date.strftime("%m/%d")
    suffix = f"({start_fmt}-{end_fmt})"

    assert result.startswith("DART ")
    assert prefix in result
    assert suffix in result

    pattern = rf"^DART {prefix} \({start_fmt}-{end_fmt}\)$"
    assert re.fullmatch(pattern, result)
