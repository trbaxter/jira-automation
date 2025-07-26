from pydantic import conint, constr, HttpUrl

def build_sprint_state_query_url(
        base_url: HttpUrl,
        board_id: conint(gt=0),
        state: constr(strip_whitespace=True, min_length=1)
) -> str:
    return f"{base_url}rest/agile/1.0/board/{board_id}/sprint?state={state}"
