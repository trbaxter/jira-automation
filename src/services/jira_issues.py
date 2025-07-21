import logging
from typing import List, Optional

import requests

from src.constants.jira_statuses import DONE_STATUSES
from src.logging_config.error_handling import handle_api_error
from src.type_defs.boardconfig import BoardConfig


def get_incomplete_stories(
        sprint_id: int,
        config: BoardConfig,
        session: requests.Session
) -> Optional[List[dict]]:
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
        url = f"{config['base_url']}/rest/agile/1.0/sprint/{sprint_id}/issue"
        params = {"startAt": start_at, "maxResults": max_results}
        response = session.get(url, params=params)

        if not handle_api_error(
                response,
                f"retrieving issues from sprint {sprint_id}"):
            return None

        data = response.json()
        issues = data.get("issues", [])

        logging.info(
            f"Fetched {len(issues)} issues from page starting at {start_at}."
        )

        incomplete_stories.extend(
            issue for issue in issues
            if issue["fields"]["status"]["name"] not in DONE_STATUSES
        )

        if len(issues) < max_results:
            break

        start_at += max_results

    logging.info(
        f"{len(incomplete_stories)} incomplete stories "
        f"found in sprint {sprint_id}."
    )
    return incomplete_stories

