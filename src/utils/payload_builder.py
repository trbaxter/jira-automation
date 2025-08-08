from datetime import datetime

from src.customtypes.shared import SAFE_STR
from src.models.sprint_close_payload import CloseSprintPayload
from src.models.sprint_start_payload import StartSprintPayload
from src.utils.datetime_format import format_jira_date


def build_close_sprint_payload(
    sprint_name: SAFE_STR, start_date: SAFE_STR, end_date: SAFE_STR
) -> CloseSprintPayload:
    return CloseSprintPayload(
        state='closed',
        name=sprint_name,
        startDate=start_date,
        endDate=end_date
    )


def build_start_sprint_payload(
    sprint_name: SAFE_STR, start_date: datetime, end_date: datetime
) -> StartSprintPayload:
    return StartSprintPayload(
        state='active',
        name=sprint_name,
        startDate=format_jira_date(start_date),
        endDate=format_jira_date(end_date),
    )
