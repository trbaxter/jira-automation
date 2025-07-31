from pydantic import BaseModel

from src.constants.shared import SAFE_STR


class CloseSprintPayload(BaseModel):
    state: SAFE_STR
    name: SAFE_STR
    startDate: SAFE_STR
    endDate: SAFE_STR
