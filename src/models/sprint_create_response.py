from pydantic import BaseModel, conint, constr


class SprintCreateResponse(BaseModel):
    id: conint(gt=0)
    self: str
    state: constr(strip_whitespace=True, min_length=1)
    name: constr(strip_whitespace=True, min_length=1)
    startDate: str
    endDate: str
    originBoardId: conint(gt=0)
