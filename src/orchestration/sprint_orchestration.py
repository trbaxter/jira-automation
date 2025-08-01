import logging
from datetime import datetime, timedelta

import requests

from src.models.board_config import BoardConfig
from src.services.jira_issues import get_incomplete_stories
from src.services.jira_sprint import (
    create_sprint,
    get_sprint_by_state,
    get_all_future_sprints,
)
from src.services.jira_sprint_closure import close_sprint
from src.services.jira_start_sprint import start_sprint
from src.services.sprint_transfer import move_issues_to_new_sprint, parse_issue
from src.utils.sprint_naming import generate_sprint_name
from src.utils.sprint_parser import parse_dart_sprint


def automate_sprint(session: requests.Session, config: BoardConfig) -> None:
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
    active_sprint = get_sprint_by_state(session, config, "active")
    future_sprints = get_all_future_sprints(session, config)

    dart_sprint = next(
        (
            sprint
            for sprint in future_sprints
            if (parsed := parse_dart_sprint(sprint["name"]))
            and parsed.start == start_date
        ),
        None,
    )

    if dart_sprint:
        logging.info(
            msg=f"\nUpcoming DART sprint found: {dart_sprint['name']}."
            "\nProceeding with automation process."
        )
        new_sprint_id = dart_sprint["id"]
        new_sprint_name = dart_sprint["name"]

    else:
        logging.warning(
            "\nNo future sprint found in the backlog starting with 'DART '."
        )

        new_sprint_name = generate_sprint_name(start_date, end_date)

        new_sprint = create_sprint(
            new_sprint_name, start_date, end_date, session
        )

        if new_sprint:
            new_sprint_id = new_sprint.get("id")
            logging.info(
                "New sprint successfully generated with sprint name: "
                f"{new_sprint_name}"
            )
        else:
            logging.error("Failed to create new sprint.")
            return

    if active_sprint:
        incomplete_stories = get_incomplete_stories(
            active_sprint["id"], config, session
        )
        incomplete_stories = [
            parse_issue(issue) for issue in incomplete_stories
        ]

        close_sprint(
            active_sprint["id"],
            active_sprint["name"],
            active_sprint["startDate"],
            active_sprint["endDate"],
            session,
            config.base_url,
        )

        move_issues_to_new_sprint(
            incomplete_stories, session, config.base_url, new_sprint_id
        )

    start_sprint(
        new_sprint_id,
        new_sprint_name,
        start_date,
        end_date,
        session,
        config.base_url,
    )
