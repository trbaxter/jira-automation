from datetime import datetime, timedelta

from utils.sprint_naming import generate_sprint_name


def test_sprint_name_generation():
    start_date = datetime(2024, 7, 1)
    end_date = start_date + timedelta(days=14)

    result = generate_sprint_name(start_date, end_date)
    assert result == "DART 240701 (07/01-07/15)"
