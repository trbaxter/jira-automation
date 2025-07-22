from src.utils.url_builder import build_sprint_state_query_url
from tests.constants.test_constants import (ACTIVE, MOCK_BASE_URL)


def test_build_sprint_state_query_url() -> None:
    url = build_sprint_state_query_url(MOCK_BASE_URL, 1, ACTIVE)

    assert url == (
        f"{MOCK_BASE_URL}/rest/agile/1.0/board/1/sprint?state={ACTIVE}"
    )