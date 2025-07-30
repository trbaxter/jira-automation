from pydantic import BaseModel

from src.constants.field_types import SAFE_STR


class StartSprintPayload(BaseModel):
    name: SAFE_STR
    startDate: SAFE_STR
    endDate: SAFE_STR
    state: SAFE_STR
