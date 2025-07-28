from pydantic import BaseModel, conint, constr


class SprintSummary(BaseModel):
    id: conint(gt=0)
    name: constr(strip_whitespace=True, min_length=1)
    state: constr(strip_whitespace=True, min_length=1)
    startDate: str | None
    endDate: str | None
    originBoardId: conint(gt=0)
