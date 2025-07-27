from datetime import datetime, timedelta

from hypothesis.strategies import text, datetimes

clean_name = text(min_size=1).filter(
    lambda s: s.strip() != "" and s == s.strip() and s.isprintable()
)

valid_date_range = datetimes(
    min_value=datetime(2025, 1, 1),
    max_value=datetime.now() + timedelta(days=365 * 100)
)

clean_string = text(min_size=1).map(str.strip).filter(
    lambda s: s != "" and s.isprintable()
)