from unittest.mock import MagicMock, patch

import requests

from src.services.sprint_transfer import (
    transfer_issue_batch_with_retry,
    transfer_all_issue_batches,
    move_issues_to_new_sprint
)
from tests.constants.patch_targets import (
    XFER_BATCH_ALL,
    XFER_EXTRACT_KEYS,
    XFER_HANDLE_ERROR,
    XFER_LOGGING,
    XFER_RETRY
)
from tests.constants.test_constants import MOCK_BASE_URL
from type_defs.jira_issue import JiraIssue


@patch(XFER_HANDLE_ERROR, return_value=True)
def test_transfer_batch_success(mock_handle: MagicMock) -> None:
    session = MagicMock(spec=requests.Session)
    response = MagicMock(spec=requests.Response)
    session.post.return_value = response

    result = transfer_issue_batch_with_retry(
        session,
        MOCK_BASE_URL,
        42,
        ["ISSUE-1", "ISSUE-2"],
        0,
        3,
        0
    )

    assert result is True
    mock_handle.assert_called_once_with(
        response, "moving issues batch from 0"
    )


@patch(XFER_HANDLE_ERROR, return_value=False)
def test_transfer_batch_failure(mock_handle: MagicMock) -> None:
    session = MagicMock(spec=requests.Session)
    session.post.return_value = MagicMock(spec=requests.Response)

    result = transfer_issue_batch_with_retry(
        session,
        MOCK_BASE_URL,
        42,
        ["ISSUE-1"],
        0,
        2,
        0
    )

    assert result is False
    assert mock_handle.call_count == 2


@patch(XFER_RETRY, return_value=True)
def test_transfer_all_batches_success(mock_transfer: MagicMock) -> None:
    session = MagicMock()
    issue_keys = [f"ISSUE-{i}" for i in range(75)]  # 2 batches: 50 + 25

    transfer_all_issue_batches(
        issue_keys,
        session,
        MOCK_BASE_URL,
        100
    )

    assert mock_transfer.call_count == 2


@patch(XFER_RETRY, side_effect=[True, False])
def test_transfer_all_batches_failure(mock_transfer: MagicMock) -> None:
    session = MagicMock()
    issue_keys = [f"ISSUE-{i}" for i in range(75)]  # 2 batches

    try:
        transfer_all_issue_batches(
            issue_keys,
            session,
            MOCK_BASE_URL,
            100
        )
        assert False, "Expected SystemExit to be raised"
    except SystemExit as e:
        assert "Transfer process aborted" in str(e)
        assert mock_transfer.call_count == 2


@patch(XFER_LOGGING)
def test_move_issues_to_new_sprint_with_no_issues(
        mock_logging: MagicMock
) -> None:
    session = MagicMock()
    move_issues_to_new_sprint(
        [],
        session,
        MOCK_BASE_URL,
        999
    )
    mock_logging.info.assert_called_with("No incomplete stories to transfer.")


@patch(XFER_BATCH_ALL)
@patch(XFER_EXTRACT_KEYS, return_value=["ISSUE-1", "ISSUE-2"])
@patch(XFER_LOGGING)
def test_move_issues_to_new_sprint_with_valid_issues(
        mock_logging: MagicMock,
        mock_extract: MagicMock,
        mock_transfer: MagicMock
) -> None:
    session = MagicMock()
    dummy_issues: list[JiraIssue] = [{"key": "ISSUE-1"}, {"key": "ISSUE-2"}]

    move_issues_to_new_sprint(
        dummy_issues,
        session,
        MOCK_BASE_URL,
        888
    )

    mock_extract.assert_called_once_with(dummy_issues)
    mock_transfer.assert_called_once_with(
        ["ISSUE-1", "ISSUE-2"],
        session,
        MOCK_BASE_URL,
        888
    )
    assert mock_logging.info.call_count >= 3
