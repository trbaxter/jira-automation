from pydantic import BaseModel

from src.fieldtypes.common import INT_GT_0, SAFE_STR


class SprintSummary(BaseModel):
    id: INT_GT_0
    name: SAFE_STR
    state: SAFE_STR
    startDate: SAFE_STR | None
    endDate: SAFE_STR | None
    originBoardId: INT_GT_0
