import pytest
from hypothesis import given
from pydantic import ValidationError

from src.constants.shared import SAFE_STR
from src.models.jira_issue import JiraIssue
from tests.strategies.shared import cleaned_string

KEY = 'key'
TYPE = 'type'
STATUS = 'status'
SUMMARY = 'summary'


@given(cleaned_string())
def test_jira_issue_valid_input(value: SAFE_STR) -> None:
    raw_data = {KEY: value, TYPE: value, STATUS: value, SUMMARY: value}
    issue = JiraIssue(**raw_data)

    for field, field_value in raw_data.items():
        assert getattr(issue, field) == field_value.strip()


@pytest.mark.parametrize(
    'field, value',
    [
        (KEY, ''),
        (KEY, '   '),
        (KEY, None),
        (TYPE, ''),
        (TYPE, '   '),
        (TYPE, None),
        (STATUS, ''),
        (STATUS, '   '),
        (STATUS, None),
        (SUMMARY, ''),
        (SUMMARY, '   '),
        (SUMMARY, None),
    ],
)
def test_jira_issue_rejects_blank_or_missing_fields(
    field: SAFE_STR, value: SAFE_STR | None
) -> None:
    valid_data = {
        KEY: 'ISSUE-1',
        TYPE: 'Bug',
        STATUS: 'Open',
        SUMMARY: 'Something broke',
    }
    invalid_data = valid_data.copy()
    invalid_data[field] = value

    with pytest.raises(ValidationError) as error:
        JiraIssue(**invalid_data)

    assert field in str(error.value)
