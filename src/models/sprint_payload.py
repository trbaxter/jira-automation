from pydantic import BaseModel, conint, constr

VALID_DATETIME_FORM = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.000\+\d{4}$"


class SprintPayload(BaseModel):
    name: constr(strip_whitespace=True, min_length=1)
    startDate: constr(pattern=VALID_DATETIME_FORM)
    endDate: constr(pattern=VALID_DATETIME_FORM)
    originBoardId: conint(gt=0)
