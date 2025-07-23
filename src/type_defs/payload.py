from typing import TypedDict


class SprintPayload(TypedDict):
    name: str
    startDate: str
    endDate: str
    originBoardId: int
