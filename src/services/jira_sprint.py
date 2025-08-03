import logging
from datetime import datetime

import requests

from src.logs.error_handling import handle_api_error
from src.models.board_config import BoardConfig
from src.models.sprint_create_response import SprintCreateResponse
from src.models.sprint_payload import SprintPayload
from src.models.sprint_summary import SprintSummary
from src.utils.config_loader import load_config
from src.utils.datetime_format import format_jira_date
from src.utils.url_builder import build_sprint_state_query_url

SPRINT_CREATE = "/rest/agile/1.0/sprint"


def build_sprint_payload(
    sprint_name: str,
    sprint_start: datetime,
    sprint_end: datetime,
    board_id: int,
) -> SprintPayload:
    return SprintPayload(
        name=sprint_name,
        startDate=format_jira_date(sprint_start),
        endDate=format_jira_date(sprint_end),
        originBoardId=board_id,
    )


def post_sprint_payload(
    session: requests.Session,
    url: str,
    payload: SprintPayload
) -> requests.Response:
    return session.post(url, json=payload.model_dump())


def parse_json_response(
    response: requests.Response,
) -> SprintCreateResponse | None:
    try:
        return response.json()
    except requests.exceptions.JSONDecodeError:
        logging.error(
            "Error: Failed to parse JSON response. "
           f"Response Content: {response.text}"
        )
        return None


def create_sprint(
    sprint_name: str,
    start_date: datetime,
    end_date: datetime,
    session: requests.Session,
) -> SprintCreateResponse | None:
    config = load_config()
    payload = build_sprint_payload(
        sprint_name,
        start_date,
        end_date,
        config.board_id
    )
    url = f"{config.base_url}{SPRINT_CREATE}"

    response = post_sprint_payload(session, url, payload)
    context = "creating sprint"

    if not handle_api_error(response, context):
        return None

    return parse_json_response(response)


def get_sprint_by_state(
    session: requests.Session,
    config: BoardConfig,
    state: str
) -> SprintSummary | None:
    url = build_sprint_state_query_url(
        config.base_url,
        config.board_id,
        state
    )
    response = session.get(url)
    context = f"retrieving {state} sprint"

    if not handle_api_error(response, context):
        return None

    sprints = response.json().get("values", [])
    return sprints[0] if sprints else None


def get_all_future_sprints(
    session: requests.Session,
    config: BoardConfig
) -> list[SprintSummary]:
    board_id = config.board_id
    start_at = 0
    max_results = 50
    all_sprints = []
    url = f"{config.base_url}/rest/agile/1.0/board/{board_id}/sprint"

    while True:
        params = {
            "state": "future",
            "startAt": start_at,
            "maxResults": max_results,
        }
        response = session.get(url, params=params)
        if response.status_code != 200:
            raise RuntimeError(
                f"Error while fetching future sprints: {response.text}"
            )

        data = response.json()
        sprints = data.get("values", [])
        all_sprints.extend(sprints)

        if data.get("isLast", True):
            break

        start_at += max_results

    return all_sprints
