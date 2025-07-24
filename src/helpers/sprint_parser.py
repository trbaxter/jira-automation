import re
from datetime import date, datetime, timedelta
from typing import NamedTuple, Optional


class DartSprint(NamedTuple):
    raw_name: str
    start: date
    end: date


_DART_RE = re.compile(
    r"""
    ^DART\                     # literal 'DART '
    (?P<yymmdd>\d{6})\         # YYMMDD then exactly one space
    \(
        (?P<start_mmdd>\d{2}/\d{2})  # 07/24
        -
        (?P<end_mmdd>\d{2}/\d{2})    # 08/06
    \)$
    """,
    re.VERBOSE,
)


def parse_dart_sprint(name: str) -> Optional[DartSprint]:
    m = _DART_RE.match(name)
    if not m:
        return None

    try:
        start = datetime.strptime(m["yymmdd"], "%y%m%d").date()
    except ValueError:
        return None


    mmdd_from_payload = start.strftime("%m/%d")
    if m["start_mmdd"] != mmdd_from_payload:
        return None

    expected_end = start + timedelta(days=13)
    if m["end_mmdd"] != expected_end.strftime("%m/%d"):
        return None

    return DartSprint(name, start, expected_end)


def is_valid_dart_sprint(name: str, ref_date: datetime) -> bool:
    sprint = parse_dart_sprint(name)
    return sprint is not None and sprint.start == ref_date.date()