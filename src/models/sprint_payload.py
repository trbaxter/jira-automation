from pydantic import BaseModel, conint, constr


class SprintPayload(BaseModel):
    name: constr(strip_whitespace=True, min_length=1)
    startDate: str
    endDate: str
    originBoardId: conint(gt=0)
