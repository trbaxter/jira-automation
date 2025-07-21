from typing import TypedDict

class CloseSprintPayload(TypedDict):
    state: str
    name: str
    startDate: str
    endDate: str
