from pydantic import BaseModel

from src.fieldtypes.common import INT_GT_0, SAFE_STR


class SprintSummary(BaseModel):
    id: INT_GT_0
    name: SAFE_STR
    state: SAFE_STR
    startDate: str | None
    endDate: str | None
    originBoardId: INT_GT_0
