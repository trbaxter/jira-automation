from pydantic import BaseModel

from src.customtypes.shared import SAFE_STR


class CloseSprintPayload(BaseModel):
    state: SAFE_STR
    name: SAFE_STR
    startDate: SAFE_STR
    endDate: SAFE_STR
