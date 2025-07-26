from pydantic import BaseModel, conint, constr, HttpUrl


class BoardConfig(BaseModel):
    board_id: conint(gt=0)
    base_url: HttpUrl
    board_name: constr(strip_whitespace=True, min_length=1)
