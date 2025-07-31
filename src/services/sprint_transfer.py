import logging
import time

import requests
from pydantic import HttpUrl

from src.constants.field_types import INT_GT_0
from src.logs.error_handling import handle_api_error
from src.models.jira_issue import JiraIssue


def transfer_issue_batch_with_retry(
    session: requests.Session,
    base_url: HttpUrl,
    sprint_id: INT_GT_0,
    issue_keys: list[str],
) -> bool:
    """
    Attempts to batch transfer issue keys to a given sprint with retry logic.

    Args:
        session: The active requests session.
        base_url: The base URL of the JIRA API.
        sprint_id: The ID of the target sprint.
        issue_keys: A list of issue keys to transfer.

    Returns:
        True if the batch was successfully transferred, False otherwise.
    """
    url = f"{base_url}/rest/agile/1.0/sprint/{sprint_id}/issue"
    payload = {"issues": issue_keys}

    for attempt in range(1, 4):
        logging.info(
            f"\nMoving batch of {len(issue_keys)} issues to sprint {sprint_id}."
            f" (Attempt {attempt} of 3)."
        )

        response = session.post(url, json=payload)
        context = f"moving issues batch"

        if handle_api_error(response, context):
            logging.info("Transfer process successful.")
            time.sleep(5)
            return True

        if attempt < 4:
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
            session, base_url, new_sprint_id, batch
        )

        if not success:
            message = (
                "Transfer process aborted. "
                f"\nFailed to move issues from index {i}"
                f" to {(i, i + len(batch) - 1)}."
            )

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

    logging.info(
        f"\nMoving the following {len(issues)} stories to the new sprint:"
    )

    for issue in issues:
        logging.info(
            f"\nIssue ID: {issue.key}"
            f"\nType: {issue.type}"
            f"\nStatus: {issue.status}"
            f"\nDescription: {issue.summary}"
        )

    issue_keys = [issue.key for issue in issues]
    transfer_all_issue_batches(issue_keys, session, base_url, new_sprint_id)


def parse_issue(raw: dict) -> JiraIssue:
    fields = raw["fields"]

    return JiraIssue(
        key=raw["key"],
        type=fields["issuetype"]["name"],
        status=fields["status"]["name"],
        summary=fields["summary"],
    )
