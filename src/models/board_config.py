from pydantic import BaseModel, HttpUrl


class BoardConfig(BaseModel):
    board_id: int
    base_url: HttpUrl
    board_name: str
