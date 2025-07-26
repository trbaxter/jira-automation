from pydantic import BaseModel, constr


class JiraIssue(BaseModel, total=True):
    key: constr(strip_whitespace=True, min_length=1)
    type: constr(strip_whitespace=True, min_length=1)
    status: constr(strip_whitespace=True, min_length=1)
    summary: constr(strip_whitespace=True, min_length=1)
