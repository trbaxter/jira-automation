import logging
from typing import List

import requests

from src.customtypes.shared import INT_GT_0
from src.logs.error_handling import handle_api_error
from src.models.board_config import BoardConfig

DONE_STATUSES = {'Done', 'Cancelled', 'Existing Solution', 'Abandoned'}


def get_incomplete_stories(
    sprint_id: INT_GT_0, config: BoardConfig, session: requests.Session
) -> List[dict] | None:
    incomplete_stories: List[dict] = []
    start_at = 0
    max_results = 50

    while True:
        url = f'{config.base_url}/rest/agile/1.0/sprint/{sprint_id}/issue'
        params = {'startAt': start_at, 'maxResults': max_results}
        response = session.get(url, params=params)
        context = f'retrieving issues from sprint {sprint_id}'

        if not handle_api_error(response, context):
            return []

        data = response.json()
        issues = data.get('issues', [])

        incomplete_stories.extend(
            issue
            for issue in issues
            if issue['fields']['status']['name'] not in DONE_STATUSES
        )

        if len(issues) < max_results:
            break

        start_at += max_results

    num_inc_stories = len(incomplete_stories)
    logging.info(
        f'\n{num_inc_stories} incomplete stories found in '
        f'previous sprint: {config.board_name}'
    )
    return incomplete_stories
