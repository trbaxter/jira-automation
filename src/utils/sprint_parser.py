import re
from datetime import date, datetime, timedelta
from typing import NamedTuple

from src.constants.field_types import SAFE_STR


class DartSprint(NamedTuple):
    raw_name: SAFE_STR
    start: date
    end: date


_DART_RE = re.compile(
    r"""
    ^DART\                           # 'DART '
    (?P<yymmdd>\d{6})\               # YYMMDD then exactly one space
    \(
        (?P<start_mmdd>\d{2}/\d{2})  # start date MM/DD
        -
        (?P<end_mmdd>\d{2}/\d{2})    # end date MM/DD
    \)$
    """,
    flags=re.VERBOSE,
)


def parse_dart_sprint(name: SAFE_STR) -> DartSprint | None:
    match = _DART_RE.match(string=name)
    if not match:
        return None

    try:
        start = datetime.strptime(match["yymmdd"], "%y%m%d").date()
    except ValueError:
        return None

    mmdd_from_payload = start.strftime(format="%m/%d")
    if match["start_mmdd"] != mmdd_from_payload:
        return None

    expected_end = start + timedelta(days=14)
    if match["end_mmdd"] != expected_end.strftime("%m/%d"):
        return None

    return DartSprint(raw_name=name, start=start, end=expected_end)


def is_valid_dart_sprint(name: SAFE_STR, ref_date: datetime) -> bool:
    sprint = parse_dart_sprint(name=name)
    return sprint is not None and sprint.start == ref_date.date()
