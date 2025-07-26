from pydantic import BaseModel, constr


class CloseSprintPayload(BaseModel):
    state: str
    name: constr(strip_whitespace=True, min_length=1)
    startDate: str
    endDate: str
