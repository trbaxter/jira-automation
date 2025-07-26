from typing import Optional
from pydantic import BaseModel, conint, constr


class SprintSummary(BaseModel):
    id: int
    name: constr(strip_whitespace=True, min_length=1)
    state: str
    startDate: Optional[str] = None
    endDate: Optional[str] = None
    originBoardId: conint(gt=0)
