from typing import TypedDict

class StartSprintPayload(TypedDict):
    name: str
    startDate: str
    endDate: str
    state: str