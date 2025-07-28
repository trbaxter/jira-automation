from datetime import datetime, timedelta

from hypothesis.strategies import text, datetimes


def valid_datetime_range():
    now = datetime.now()
    hundred_years_later = datetime.now() + timedelta(days=365 * 100)

    return datetimes(min_value=now, max_value=hundred_years_later)


def cleaned_string():
    min_str = text(min_size=1)

    return min_str.map(str.strip).filter(
        lambda string: string != "" and string.isprintable()
    )
