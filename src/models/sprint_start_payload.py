from pydantic import BaseModel

from src.customtypes.shared import SAFE_STR


class StartSprintPayload(BaseModel):
    name: SAFE_STR
    startDate: SAFE_STR
    endDate: SAFE_STR
    state: SAFE_STR
