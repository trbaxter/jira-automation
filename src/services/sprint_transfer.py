import logging
import time

import requests
from pydantic import HttpUrl

from src.constants.field_types import INT_GT_0, INT_GEQ_0
from src.logs.error_handling import handle_api_error
from src.models.jira_issue import JiraIssue


def transfer_issue_batch_with_retry(
    session: requests.Session,
    base_url: HttpUrl,
    sprint_id: INT_GT_0,
    issue_keys: list[str],
    batch_start_index: INT_GEQ_0,
    max_attempts: INT_GEQ_0 = 3,
    cooldown_seconds: INT_GEQ_0 = 5,
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
            "\nMoving batch of %d issues (index %d to %d) to sprint %d. "
            "Attempt %d of %d.",
            len(issue_keys),
            batch_start_index,
            batch_start_index + len(issue_keys) - 1,
            sprint_id,
            attempt,
            max_attempts,
        )

        response = session.post(url, json=payload)
        context = f"moving issues batch from {batch_start_index}"

        if handle_api_error(response, context):
            logging.info("Transfer process successful.")
            time.sleep(cooldown_seconds)
            return True

        if attempt < max_attempts:
            logging.info("\nTransfer failed. Retrying...")
        else:
            logging.error("Transfer failed. Max attempts exceeded.")

    return False


def transfer_all_issue_batches(
    issue_keys: list[str],
    session: requests.Session,
    base_url: HttpUrl,
    new_sprint_id: INT_GT_0,
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
    start_index = 0
    stop_index = len(issue_keys)
    batch_size = 50

    for i in range(start_index, stop_index, batch_size):
        batch = issue_keys[i : i + batch_size]
        success = transfer_issue_batch_with_retry(
            session=session,
            base_url=base_url,
            sprint_id=new_sprint_id,
            issue_keys=batch,
            batch_start_index=i,
        )

        if not success:
            message = (
                "Transfer process aborted. "
                "\nFailed to move issues from index %d to %d."
            ) % (i, i + len(batch) - 1)

            raise SystemExit(message)

    logging.info("Migration of unfinished stories complete.")


def move_issues_to_new_sprint(
    issues: list[JiraIssue],
    session: requests.Session,
    base_url: HttpUrl,
    new_sprint_id: INT_GT_0,
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

    num_issues = len(issues)

    logging.info(
        f"\nMoving the following {num_issues} stories to the new sprint:"
    )

    for issue in issues:
        logging.info(
            "\nIssue ID: %s" "\nType: %s" "\nStatus: %s" "\nSummary: %s",
            issue.key,
            issue.type,
            issue.status,
            issue.summary,
        )

    issue_keys = [issue.key for issue in issues]

    transfer_all_issue_batches(
        issue_keys=issue_keys,
        session=session,
        base_url=base_url,
        new_sprint_id=new_sprint_id,
    )


def parse_issue(raw: dict) -> JiraIssue:
    fields = raw.get("fields", {})

    return JiraIssue(
        key=raw.get("key", "UNKNOWN"),
        type=fields.get("issuetype", {}).get("name") or "Unknown",
        status=fields.get("status", {}).get("name") or "Unknown",
        summary=(fields.get("summary") or "").strip(),
    )
