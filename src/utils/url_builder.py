from pydantic import HttpUrl

from src.constants.shared import INT_GT_0, SAFE_STR


def build_sprint_state_query_url(
    base_url: HttpUrl,
    board_id: INT_GT_0,
    state: SAFE_STR
) -> SAFE_STR:
    return f'{base_url}rest/agile/1.0/board/{board_id}/sprint?state={state}'
