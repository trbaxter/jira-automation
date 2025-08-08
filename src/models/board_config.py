from pydantic import BaseModel, HttpUrl

from src.customtypes.shared import SAFE_STR, PositiveInt


class BoardConfig(BaseModel):
    board_id: PositiveInt
    base_url: HttpUrl
    board_name: SAFE_STR
