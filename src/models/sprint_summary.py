from typing import TypedDict, Optional


class SprintSummary(TypedDict):
    id: int
    name: str
    state: str
    startDate: Optional[str]
    endDate: Optional[str]
    originBoardId: int
