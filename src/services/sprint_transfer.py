import logging
import time

import requests

from src.logging_config.error_handling import handle_api_error
from src.type_defs.jira_issue import JiraIssue


def transfer_issue_batch_with_retry(
        session: requests.Session,
        base_url: str,
        sprint_id: int,
        issue_keys: list[str],
        batch_start_index: int,
        max_attempts: int = 3,
        cooldown_seconds: int = 5
) -> bool:
    """
    Attempts to batch transfer issue keys to a given sprint with retry logic.

    Args:
        session: The active requests session.
        base_url: The base URL of the JIRA API.
        sprint_id: The ID of the target sprint.
        issue_keys: A list of issue keys to transfer.
        batch_start_index: Index of the first issue in the batch (for logging).
        max_attempts: Maximum retry attempts before failing.
        cooldown_seconds: Delay between successful batch transfers.

    Returns:
        True if the batch was successfully transferred, False otherwise.
    """
    url = f"{base_url}/rest/agile/1.0/sprint/{sprint_id}/issue"
    payload = {"issues": issue_keys}

    for attempt in range(1, max_attempts + 1):
        logging.info(
            f"\nTransferring batch of {len(issue_keys)} issues "
            f"(index {batch_start_index} to "
            f"{batch_start_index + len(issue_keys) - 1}) "
            f"to sprint {sprint_id}. Attempt {attempt} of {max_attempts}."
        )

        response = session.post(url, json=payload)

        if handle_api_error(
                response,
                f"moving issues batch from {batch_start_index}"):
            logging.info("Transfer process successful.")
            time.sleep(cooldown_seconds)
            return True

        logging.error(
            "Transfer failed. Will retry if not exceeded max attempts."
        )

    return False


def transfer_all_issue_batches(
        issue_keys: list[str],
        session: requests.Session,
        base_url: str,
        new_sprint_id: int
) -> None:
    """
    Iterates through issue keys in batches and transfers them to a new sprint.

    Args:
        issue_keys: List of issue key strings.
        session: Authenticated requests session.
        base_url: Base URL of the JIRA API.
        new_sprint_id: ID of the target sprint.

    Raises:
        SystemExit: If any batch fails after all retry attempts.
    """
    batch_size = 50

    for i in range(0, len(issue_keys), batch_size):
        batch = issue_keys[i:i + batch_size]
        success = transfer_issue_batch_with_retry(
            session,
            base_url,
            new_sprint_id,
            batch,
            i
        )

        if not success:
            raise SystemExit(
                f"Transfer process aborted. "
                f"\nFailed to move issues from index {i} to "
                f"{i + len(batch) - 1}."
            )

    logging.info("Migration of unfinished stories complete.")


def move_issues_to_new_sprint(
        issues: list[JiraIssue],
        session: requests.Session,
        base_url: str,
        new_sprint_id: int
) -> None:
    """
    Coordinates the transfer of JIRA issues to a new sprint in batches.

    Args:
        issues: List of JIRA issue dictionaries.
        session: Authenticated requests session.
        base_url: Base URL for JIRA API.
        new_sprint_id: ID of the sprint to move issues to.

    Returns:
        None.
    """
    if not issues:
        logging.info("No incomplete stories to transfer.")
        return

    logging.info(
        f"\nMoving the following {len(issues)} stories to the new sprint:"
    )

    for issue in issues:
        logging.info(
            f"\nIssue ID: {issue['key']}"
            f"\nType: {issue.get('type', 'Unknown')}"
            f"\nStatus: {issue.get('status', 'Unknown')}"
            f"\nSummary: {issue.get('summary', '').strip()}"
        )

    issue_keys = [issue["key"] for issue in issues]

    transfer_all_issue_batches(issue_keys, session, base_url, new_sprint_id)


def parse_issue(raw: dict) -> JiraIssue:
    return {
        "key":
            raw["key"],
        "type":
            raw.get("fields", {}).get("issuetype", {}).get("name", "Unknown"),
        "status":
            raw.get("fields", {}).get("status", {}).get("name", "Unknown"),
        "summary":
            raw.get("fields", {}).get("summary", "").strip()
    }
