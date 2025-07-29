from pydantic import HttpUrl

from src.fieldtypes.common import INT_GT_0, SAFE_STR


def build_sprint_state_query_url(
    base_url: HttpUrl, board_id: INT_GT_0, state: SAFE_STR
) -> str:
    return f"{base_url}rest/agile/1.0/board/{board_id}/sprint?state={state}"
