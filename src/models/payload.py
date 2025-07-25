from pydantic import BaseModel


class SprintPayload(BaseModel):
    name: str
    startDate: str
    endDate: str
    originBoardId: int
