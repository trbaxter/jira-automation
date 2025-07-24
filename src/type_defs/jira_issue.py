from typing import TypedDict


class JiraIssue(TypedDict, total=True):
    key: str
    type: str
    status: str
    summary: str