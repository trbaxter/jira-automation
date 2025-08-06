from datetime import datetime, timedelta

from hypothesis.strategies import composite
from hypothesis.strategies import text, datetimes, SearchStrategy

from src.models.credentials import Credentials


@composite
def valid_credentials(draw):
    email = draw(cleaned_string())
    token = draw(cleaned_string())
    return Credentials(email=email, token=token)


def valid_datetime_range() -> SearchStrategy[datetime]:
    now = datetime.now()
    hundred_years_later = now + timedelta(days=365 * 100)
    return datetimes(now, hundred_years_later)


def cleaned_string() -> SearchStrategy[str]:
    return (
        text(min_size=1)
        .map(str.strip)
        .filter(lambda string: string != '' and string.isprintable())
    )
