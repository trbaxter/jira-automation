from pydantic import BaseModel

from src.customtypes.shared import INT_GT_0, JIRA_DATETIME_STR, SAFE_STR


class SprintPayload(BaseModel):
    name: SAFE_STR
    startDate: JIRA_DATETIME_STR
    endDate: JIRA_DATETIME_STR
    originBoardId: INT_GT_0
