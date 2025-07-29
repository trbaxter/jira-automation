import logging
from datetime import datetime, timedelta

import requests

from src.services.jira_issues import get_incomplete_stories
from src.services.jira_sprint import (
    create_sprint,
    get_sprint_by_state,
    get_all_future_sprints,
)
from src.services.jira_sprint_closure import close_sprint
from src.services.jira_start_sprint import start_sprint
from src.services.sprint_transfer import move_issues_to_new_sprint, parse_issue
from src.utils.config_loader import load_config
from src.utils.sprint_naming import generate_sprint_name
from src.utils.sprint_parser import parse_dart_sprint


def automate_sprint(session: requests.Session) -> None:
    """
    Orchestrates the full Jira sprint lifecycle:
    • Creates or fetches the next sprint
    • Closes the current one (if active)
    • Transfers incomplete stories
    • Activates the new sprint
    """
    logging.info(msg="\nBeginning sprint automation process...")

    start_date = datetime.now()
    end_date = start_date + timedelta(days=14)
    config = load_config()
    future_sprints = get_all_future_sprints(session=session, config=config)

    dart_sprint = next(
        (
            sprint
            for sprint in future_sprints
            if (parsed := parse_dart_sprint(name=sprint["name"]))
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
            msg="\nNo future sprint found in the backlog starting with 'DART '."
            "\nInitializing sprint generation."
        )

        new_sprint_name = generate_sprint_name(
            start_date=start_date, end_date=end_date
        )

        new_sprint = create_sprint(
            sprint_name=new_sprint_name,
            start_date=start_date,
            end_date=end_date,
            session=session,
        )

        if not new_sprint:
            logging.error(msg="Failed to create new sprint.")
            return

        new_sprint_id = new_sprint.get("id")

    active_sprint = get_sprint_by_state(
        session=session, config=config, state="active"
    )

    if active_sprint:
        incomplete_stories = get_incomplete_stories(
            sprint_id=active_sprint["id"], config=config, session=session
        )
        incomplete_stories = [
            parse_issue(issue) for issue in incomplete_stories
        ]

        close_sprint(
            sprint_id=active_sprint["id"],
            sprint_name=active_sprint["name"],
            start_date=active_sprint["startDate"],
            end_date=active_sprint["endDate"],
            session=session,
            base_url=config.base_url,
        )

        move_issues_to_new_sprint(
            issues=incomplete_stories,
            session=session,
            base_url=config.base_url,
            new_sprint_id=new_sprint_id,
        )

    start_sprint(
        new_sprint_id=new_sprint_id,
        sprint_name=new_sprint_name,
        start_date=start_date,
        end_date=end_date,
        session=session,
        base_url=config.base_url,
    )
