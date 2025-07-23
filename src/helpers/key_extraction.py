from src.type_defs.jira_issue import JiraIssue


def extract_issue_keys(issues: list[JiraIssue]) -> list[str]:
    """
    Extracts the issue keys from a list of JIRA issue dictionaries.

    Args:
        issues: A list of JIRA issue dictionaries.

    Returns:
        A list of issue key strings.
    """
    return [issue["key"] for issue in issues]
