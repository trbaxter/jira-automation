from src.utils.url_builder import build_sprint_state_query_url

BASE_URL = "https://example.atlassian.net"
ACTIVE = "active"
ID = 10

def test_build_sprint_state_query_url() -> None:
    url = build_sprint_state_query_url(
        base_url=BASE_URL,
        board_id=ID,
        state=ACTIVE
    )

    assert url == f"{BASE_URL}/rest/agile/1.0/board/{ID}/sprint?state={ACTIVE}"