from datetime import datetime, timedelta

import pytest

from src.utils.sprint_parser import parse_dart_sprint, is_valid_dart_sprint

VALID_SPRINT = "DART 250728 (07/28-08/11)"
REF_DATE = datetime(2025, 7, 28)


def test_parse_valid_sprint_returns_object() -> None:
    result = parse_dart_sprint(VALID_SPRINT)
    assert result is not None
    assert result.raw_name == VALID_SPRINT
    assert result.start == REF_DATE.date()
    assert result.end == REF_DATE.date() + timedelta(days=14)


@pytest.mark.parametrize(
    "invalid_name",
    [
        "dart 250728 (07/28-08/11)",  # lowercase
        "DART250728 (07/28-08/11)",  # no space
        "DART 25072807/28-08/11)",  # missing parenthesis
        "DART 250728 (07/27-08/11)",  # wrong start MM/DD
        "DART 250728 (07/28-08/09)",  # wrong end MM/DD
        "DART 991399 (13/99-14/12)",  # invalid calendar date
        "CN DART 250728 (07/28-08/11)",  # sprint for different board
        "DART 25728 (7/27-8/10)",  # missing date leading zero
    ],
)
def test_parse_invalid_returns_none(invalid_name: str) -> None:
    assert parse_dart_sprint(name=invalid_name) is None


def test_is_valid_dart_sprint_true() -> None:
    assert is_valid_dart_sprint(name=VALID_SPRINT, ref_date=REF_DATE) is True


def test_is_valid_dart_sprint_false_on_date_mismatch() -> None:
    bad_date = REF_DATE - timedelta(days=1)
    assert is_valid_dart_sprint(name=VALID_SPRINT, ref_date=bad_date) is False


def test_is_valid_dart_sprint_false_on_parse_fail() -> None:
    assert (
            is_valid_dart_sprint(name="INVALID STRING",
                                 ref_date=REF_DATE) is False
    )
