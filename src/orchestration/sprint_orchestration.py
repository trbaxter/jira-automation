import logging
from datetime import datetime, timedelta
from typing import cast

import requests

from src.helpers.config_accessor import get_board_config
from src.helpers.sprint_naming import generate_sprint_name
from src.services.jira_issues import get_incomplete_stories
from src.services.jira_sprint import create_sprint, get_sprint_by_state
from src.services.jira_sprint_closure import close_sprint
from src.services.jira_start_sprint import start_sprint
from src.services.sprint_transfer import move_issues_to_new_sprint
from src.type_defs.jira_issue import JiraIssue
from src.type_defs.boardconfig import BoardConfig


def automate_sprint(board_name: str, session: requests.Session) -> None:
    """
    Orchestrates the full Jira sprint lifecycle:
    • Creates or fetches the next sprint
    • Closes the current one (if active)
    • Transfers incomplete stories
    • Activates the new sprint
    """
    logging.info("\nBeginning sprint automation process...\n")

    start_date = datetime.now()
    end_date = start_date + timedelta(days=14)
    config: BoardConfig = get_board_config(board_name)
    upcoming_sprint = get_sprint_by_state(session, config, "future")

    if upcoming_sprint and upcoming_sprint["name"].startswith("DART "):
        logging.info(
            f"Upcoming sprint found: {upcoming_sprint['name']}. "
            f"Proceeding with this sprint."
        )
        new_sprint_id = upcoming_sprint["id"]
        new_sprint_name = upcoming_sprint["name"]
    else:
        if upcoming_sprint:
            logging.warning(
                "No future sprints found starting with DART. "
                "Creating new DART sprint."
            )
        else:
            logging.info(
                "No upcoming sprint found. Initializing sprint creation."
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
            logging.error("Failed to create a new sprint.")
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
