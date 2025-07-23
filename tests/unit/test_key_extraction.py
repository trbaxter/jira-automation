from src.helpers.key_extraction import extract_issue_keys
from type_defs.jira_issue import JiraIssue


def test_extract_issue_keys() -> None:
    issues: list[JiraIssue] = [
        {"key": "Issue_1"},
        {"key": "Issue_2"},
        {"key": "Issue_3"}
    ]
    result = extract_issue_keys(issues)
    assert result == ["Issue_1", "Issue_2", "Issue_3"]
