import pytest
from hypothesis import given
from hypothesis.strategies import integers
from pydantic import ValidationError

from src.models.sprint_summary import SprintSummary
from strategies.common import cleaned_string

VALID_SUMMARY = {
    "id": 1,
    "name": "Sprint 100",
    "state": "active",
    "startDate": "2024-11-01T00:00:00.000+0000",
    "endDate": "2024-11-14T23:59:59.000+0000",
    "originBoardId": 42,
}


@given(cleaned_string())
def test_name_accepts_valid_clean_strings(name: str) -> None:
    model = SprintSummary(**{**VALID_SUMMARY, "name": name})
    assert model.name == name


@given(integers(1))
def test_positive_id_accepted(id_value: int) -> None:
    model = SprintSummary(**{**VALID_SUMMARY, "id": id_value})
    assert model.id == id_value


def test_valid_summary_constructs_object() -> None:
    model = SprintSummary(**VALID_SUMMARY)
    assert isinstance(model, SprintSummary)
    assert model.model_dump() == VALID_SUMMARY


@pytest.mark.parametrize("bad_id", [0, -1, "abc", None])
def test_invalid_id_raises(bad_id) -> None:
    with pytest.raises(expected_exception=ValidationError):
        SprintSummary(**{**VALID_SUMMARY, "id": bad_id})


@pytest.mark.parametrize("bad_name", ["", "   "])
def test_invalid_name_raises(bad_name) -> None:
    with pytest.raises(expected_exception=ValidationError):
        SprintSummary(**{**VALID_SUMMARY, "name": bad_name})


@pytest.mark.parametrize("bad_state", ["", "   "])
def test_invalid_state_raises(bad_state) -> None:
    with pytest.raises(expected_exception=ValidationError):
        SprintSummary(**{**VALID_SUMMARY, "state": bad_state})


@pytest.mark.parametrize("bad_board", [0, -1, None])
def test_invalid_origin_board_id_raises(bad_board) -> None:
    with pytest.raises(expected_exception=ValidationError):
        SprintSummary(**{**VALID_SUMMARY, "originBoardId": bad_board})


@pytest.mark.parametrize("nullable_field", ["startDate", "endDate"])
def test_optional_date_fields_accept_none(nullable_field: str) -> None:
    model = SprintSummary(**{**VALID_SUMMARY, nullable_field: None})
    assert getattr(model, nullable_field) is None
