from unittest.mock import MagicMock, patch

import pytest
from _pytest.logging import LogCaptureFixture
from _pytest.monkeypatch import MonkeyPatch
from hypothesis import given
from hypothesis.strategies import composite, DrawFn
from pydantic import HttpUrl

from src.models.jira_issue import JiraIssue
from src.services.sprint_transfer import (
    parse_issue,
    transfer_issue_batch_with_retry,
    transfer_all_issue_batches,
    move_issues_to_new_sprint,
)
from strategies.common import cleaned_string


@composite
def raw_issue_strategy(draw: DrawFn) -> dict[str, object]:
    return {
        "key": draw(cleaned_string()),
        "fields": {
            "summary": draw(cleaned_string()),
            "status": {"name": draw(cleaned_string())},
            "issuetype": {"name": draw(cleaned_string())},
        },
    }


@given(raw=raw_issue_strategy())
def test_parse_issue_handles_missing_fields(raw: dict[str, object]) -> None:
    result = parse_issue(raw)

    assert isinstance(result, JiraIssue)
    assert result.key == raw.get("key", "UNKNOWN")

    fields = raw.get("fields", {})
    assert isinstance(fields, dict)

    issuetype = fields.get("issuetype", {})
    if isinstance(issuetype, dict):
        expected_type = issuetype.get("name") or "Unknown"
    else:
        expected_type = "Unknown"

    status = fields.get("status", {})
    if isinstance(status, dict):
        expected_status = status.get("name") or "Unknown"
    else:
        expected_status = "Unknown"

    summary = fields.get("summary", "")
    expected_summary = summary.strip() if isinstance(summary, str) else ""

    assert result.type == expected_type
    assert result.status == expected_status
    assert result.summary == expected_summary


def test_transfer_batch_success_first_try() -> None:
    session = MagicMock()
    session.post.return_value = MagicMock()

    with (
        patch(
            target="src.services.sprint_transfer.handle_api_error",
            return_value=True,
        ),
        patch(target="time.sleep", return_value=None),
    ):
        result = transfer_issue_batch_with_retry(
            session=session,
            base_url=HttpUrl("https://mock.atlassian.net"),
            sprint_id=1,
            issue_keys=["ISSUE-1"],
            batch_start_index=0,
        )
        assert result is True


def test_transfer_batch_fails_all_attempts() -> None:
    session = MagicMock()
    session.post.return_value = MagicMock()

    with patch(
        target="src.services.sprint_transfer.handle_api_error",
        return_value=False,
    ):
        result = transfer_issue_batch_with_retry(
            session=session,
            base_url=HttpUrl("https://mock.atlassian.net"),
            sprint_id=1,
            issue_keys=["ISSUE-1"],
            batch_start_index=0,
            max_attempts=2,
            cooldown_seconds=0,
        )
        assert result is False


def test_transfer_all_batches_success(monkeypatch: MonkeyPatch) -> None:
    mock_transfer = MagicMock(return_value=True)
    monkeypatch.setattr(
        target="src.services.sprint_transfer.transfer_issue_batch_with_retry",
        name=mock_transfer,
    )

    transfer_all_issue_batches(
        issue_keys=["A", "B", "C", "D", "E"],
        session=MagicMock(),
        base_url=HttpUrl("https://mock.atlassian.net"),
        new_sprint_id=123,
    )

    assert mock_transfer.call_args[1]["issue_keys"] == ["A", "B", "C", "D", "E"]


def test_transfer_batch_fails_raises_exit(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr(
        target="src.services.sprint_transfer.transfer_issue_batch_with_retry",
        name=(lambda *a, **kw: False),
    )

    with pytest.raises(expected_exception=SystemExit) as exit_info:
        transfer_all_issue_batches(
            issue_keys=["A", "B"],
            session=MagicMock(),
            base_url=HttpUrl("https://mock.atlassian.net"),
            new_sprint_id=123,
        )
    assert "Transfer process aborted." in str(object=exit_info.value)


def test_move_issues_logs_and_transfers(
    monkeypatch: MonkeyPatch, caplog: LogCaptureFixture
) -> None:
    called = {}

    def mock_transfer_all(issue_keys, **_kwargs):
        called["keys"] = issue_keys

    monkeypatch.setattr(
        target="src.services.sprint_transfer.transfer_all_issue_batches",
        name=mock_transfer_all,
    )

    move_issues_to_new_sprint(
        issues=[
            JiraIssue(
                key="KEY-1", type="Bug", status="To Do", summary="Fix stuff"
            )
        ],
        session=MagicMock(),
        base_url=HttpUrl("https://mock.atlassian.net"),
        new_sprint_id=999,
    )

    assert called["keys"] == ["KEY-1"]
    assert "Moving the following 1 stories" in caplog.text


def test_move_issues_exits_gracefully_on_empty(
    caplog: LogCaptureFixture,
) -> None:
    move_issues_to_new_sprint(
        issues=[],
        session=MagicMock(),
        base_url=HttpUrl("https://mock.atlassian.net"),
        new_sprint_id=999,
    )
    assert "No incomplete stories to transfer." in caplog.text
