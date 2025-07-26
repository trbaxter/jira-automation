from pydantic import HttpUrl

from src.utils.url_builder import build_sprint_state_query_url

_MOCK_BASE_URL = HttpUrl("https://mock.com/")
_MOCK_FULL_URL = "https://mock.com/rest/agile/1.0/board/1/sprint?state=active"


def test_build_sprint_state_query_url() -> None:
    url = build_sprint_state_query_url(
        base_url=_MOCK_BASE_URL,
        board_id=1,
        state="active"
    )

    assert url == _MOCK_FULL_URL
