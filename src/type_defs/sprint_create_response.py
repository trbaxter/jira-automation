from typing import TypedDict

class SprintCreateResponse(TypedDict):
    id: int
    self: str
    state: str
    name: str
    startDate: str
    endDate: str
    originBoardId: int