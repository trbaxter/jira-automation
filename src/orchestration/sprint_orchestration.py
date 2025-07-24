import logging
from datetime import datetime, timedelta
from typing import cast

import requests

from src.helpers.config_accessor import get_board_config
from src.helpers.is_valid_dart_sprint import is_valid_dart_sprint
from src.helpers.sprint_naming import generate_sprint_name
from src.services.jira_issues import get_incomplete_stories
from src.services.jira_sprint import (
    create_sprint,
    get_sprint_by_state,
    get_all_future_sprints
)
from src.services.jira_sprint_closure import close_sprint
from src.services.jira_start_sprint import start_sprint
from src.services.sprint_transfer import move_issues_to_new_sprint
from src.type_defs.jira_issue import JiraIssue


def automate_sprint(board_name: str, session: requests.Session) -> None:
    """
    Orchestrates the full Jira sprint lifecycle:
    • Creates or fetches the next sprint
    • Closes the current one (if active)
    • Transfers incomplete stories
    • Activates the new sprint
    """
    logging.info("\nBeginning sprint automation process...")

    start_date = datetime.now()
    end_date = start_date + timedelta(days=14)
    config = get_board_config(board_name)
    future_sprints = get_all_future_sprints(session, config)

    dart_sprint = next(
        (s for s in sorted(future_sprints, key=lambda x: x.get("startDate", ""))
         if is_valid_dart_sprint(
            s["name"],
            datetime.fromisoformat(s["startDate"][:-1])
            if "startDate" in s and s["startDate"]
            else datetime.now()
        )
         ),
        None
    )

    if dart_sprint:
        logging.info(
            f"\nUpcoming DART sprint found: {dart_sprint['name']}"
            "Proceeding with automation process."
        )
        new_sprint_id = dart_sprint["id"]
        new_sprint_name = dart_sprint["name"]
    else:
        logging.warning(
            "\nNo future sprint found in the backlog starting with 'DART '. "
            "Initializing sprint generation."
        )
        new_sprint_name = generate_sprint_name(start_date, end_date)
        new_sprint = create_sprint(
            board_name,
            new_sprint_name,
            start_date,
            end_date,
            session
        )
        if not new_sprint:
            logging.error("Failed to create new sprint.")
            return
        new_sprint_id = new_sprint.get("id")

    active_sprint = get_sprint_by_state(session, config, "active")
    if active_sprint:
        incomplete_stories = get_incomplete_stories(
            active_sprint["id"],
            config,
            session
        )
        incomplete_stories = cast(list[JiraIssue], incomplete_stories)

        close_sprint(
            active_sprint["id"],
            active_sprint["name"],
            active_sprint["startDate"],
            active_sprint["endDate"],
            session,
            config["base_url"]
        )

        move_issues_to_new_sprint(
            incomplete_stories,
            session,
            config["base_url"],
            new_sprint_id
        )

    start_sprint(
        new_sprint_id,
        new_sprint_name,
        start_date,
        end_date,
        session,
        config["base_url"]
    )
