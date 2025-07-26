from pydantic import BaseModel, constr


class SprintPayload(BaseModel):
    name: constr(strip_whitespace=True, min_length=1)
    startDate: str
    endDate: str
    originBoardId: int
