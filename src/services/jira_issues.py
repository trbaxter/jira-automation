import logging
from typing import List

import requests
from pydantic import conint

from src.logging_config.error_handling import handle_api_error
from src.models.board_config import BoardConfig

DONE_STATUSES = {"Done", "Cancelled", "Existing Solution", "Abandoned"}


def get_incomplete_stories(
        sprint_id: conint(gt=0), config: BoardConfig, session: requests.Session
) -> List[dict] | None:
    """
    Retrieves all incomplete stories from the specified sprint.

    Collects all stories from a sprint if the story status isn't found in
    the DONE_STATUSES set, indicating the story is carrying-over.

    Args:
        sprint_id: The active sprint ID.
        config: BoardConfig for the current Jira board.
        session: An authenticated requests.Session instance.

    Returns:
        A list of incomplete issue dictionaries, or None if the API call fails.
    """
    incomplete_stories: List[dict] = []
    start_at = 0
    max_results = 50

    while True:
        url = f"{config.base_url}/rest/agile/1.0/sprint/{sprint_id}/issue"
        params = {"startAt": start_at, "maxResults": max_results}
        response = session.get(url=url, params=params)
        context = f"retrieving issues from sprint {sprint_id}"

        if not handle_api_error(response=response, context=context):
            return []

        data = response.json()
        issues = data.get("issues", [])

        logging.info(
            "\nFetched %d issues from page starting at %d.",
            len(issues),
            start_at,
        )

        incomplete_stories.extend(
            issue
            for issue in issues
            if issue["fields"]["status"]["name"] not in DONE_STATUSES
        )

        if len(issues) < max_results:
            break

        start_at += max_results

    logging.info(
        "%d incomplete stories found in sprint %d.",
        len(incomplete_stories),
        sprint_id,
    )
    return incomplete_stories
