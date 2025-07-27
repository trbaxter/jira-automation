from datetime import datetime, timedelta

from hypothesis.strategies import text, datetimes

_NOW = datetime.now()
_HUNDRED_YEARS = datetime.now() + timedelta(days=365 * 100)

valid_date_range = datetimes(min_value=_NOW, max_value=_HUNDRED_YEARS)

clean_string = (
    text(min_size=1)
    .map(str.strip)
    .filter(lambda string: string != "" and string.isprintable())
)
