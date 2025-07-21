from src.type_defs.sprint_close_payload import CloseSprintPayload
from src.type_defs.sprint_start_payload import StartSprintPayload
from src.utils.datetime_format import format_jira_date
from datetime import datetime


def build_close_sprint_payload(
        sprint_name: str,
        start_date: str,
        end_date: str
) -> CloseSprintPayload:
    return {
        "state": "closed",
        "name": sprint_name,
        "startDate": start_date,
        "endDate": end_date,
    }


def build_start_sprint_payload(
        sprint_name: str,
        start_date: datetime,
        end_date: datetime
) -> StartSprintPayload:
    return {
        "state": "active",
        "name": sprint_name,
        "startDate": format_jira_date(start_date),
        "endDate": format_jira_date(end_date)
    }

