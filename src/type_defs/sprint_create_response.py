from typing import TypedDict, Literal

class SprintCreateResponse(TypedDict):
    id: int
    self: str
    state: Literal["future", "active", "closed"]
    name: str
    startDate: str
    endDate: str
    originBoardId: int