import logging
from datetime import datetime, timedelta
from typing import cast
from src.type_defs.jira_issue import JiraIssue

import requests

from src.helpers.config_accessor import get_board_config
from src.services.jira_sprint import create_sprint, get_sprint_by_state
from src.services.jira_sprint_closure import close_sprint
from src.services.sprint_transfer import move_issues_to_new_sprint
from src.services.jira_issues import get_incomplete_stories
from src.services.jira_start_sprint import start_sprint
from src.helpers.sprint_naming import generate_sprint_name
from type_defs.boardconfig import BoardConfig


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
    config: BoardConfig = get_board_config(board_name=board_name)
    upcoming_sprint = get_sprint_by_state(
        session=session,
        config=config,
        state="future"
    )

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
                f"Ignoring non-DART sprint '{upcoming_sprint['name']}' "
                f"— creating a new department-standard sprint instead."
            )
        else:
            logging.info(
                "No upcoming sprint found — creating a new DART sprint."
            )
        new_sprint_name = generate_sprint_name(start_date, end_date)
        new_sprint = create_sprint(
            board_name=board_name,
            sprint_name=new_sprint_name,
            start_date=start_date,
            end_date=end_date,
            session=session
        )
        if not new_sprint:
            logging.error("Failed to create a new sprint.")
            return
        new_sprint_id = new_sprint.get("id")

    active_sprint = get_sprint_by_state(
        session=session,
        config=config,
        state="active"
    )
    if active_sprint:
        incomplete_stories = get_incomplete_stories(
            sprint_id=active_sprint["id"],
            config=config,
            session=session
        )
        incomplete_stories = cast(list[JiraIssue], incomplete_stories)

        close_sprint(
            sprint_id = active_sprint["id"],
            sprint_name = active_sprint["name"],
            start_date = active_sprint["startDate"],
            end_date = active_sprint["endDate"],
            session = session,
            base_url = config["base_url"]
        )

        move_issues_to_new_sprint(
            issues=incomplete_stories,
            session=session,
            base_url=config["base_url"],
            new_sprint_id=new_sprint_id
        )

    start_sprint(
        new_sprint_id=new_sprint_id,
        sprint_name=new_sprint_name,
        start_date=start_date,
        end_date=end_date,
        session=active_sprint["session"],
        base_url=active_sprint["base_url"]
    )
