from pydantic import BaseModel, constr


class StartSprintPayload(BaseModel):
    name: constr(strip_whitespace=True, min_length=1)
    startDate: constr(strip_whitespace=True, min_length=1)
    endDate: constr(strip_whitespace=True, min_length=1)
    state: constr(strip_whitespace=True, min_length=1)
