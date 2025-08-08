from pydantic import BaseModel

from src.customtypes.shared import SAFE_STR, INT_GT_0


class SprintCreateResponse(BaseModel):
    id: INT_GT_0
    self: SAFE_STR
    state: SAFE_STR
    name: SAFE_STR
    startDate: str
    endDate: str
    originBoardId: INT_GT_0
