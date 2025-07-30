from datetime import datetime, timedelta

from hypothesis.strategies import text, datetimes, SearchStrategy


def valid_datetime_range() -> SearchStrategy[datetime]:
    now = datetime.now()
    hundred_years_later = now + timedelta(days=365 * 100)
    return datetimes(now, hundred_years_later)


def cleaned_string() -> SearchStrategy[str]:
    return (
        text(min_size=1)
        .map(str.strip)
        .filter(lambda string: string != "" and string.isprintable())
    )
