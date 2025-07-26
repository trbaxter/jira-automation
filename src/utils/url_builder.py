from pydantic import HttpUrl

def build_sprint_state_query_url(
        base_url: HttpUrl,
        board_id: int,
        state: str
) -> str:
    return f"{base_url}rest/agile/1.0/board/{board_id}/sprint?state={state}"
