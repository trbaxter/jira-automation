from pydantic import BaseModel

from src.constants.field_types import SAFE_STR


class JiraIssue(BaseModel):
    key: SAFE_STR
    type: SAFE_STR
    status: SAFE_STR
    summary: SAFE_STR
