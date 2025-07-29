from pydantic import BaseModel, HttpUrl

from src.fieldtypes.common import SAFE_STR, INT_GT_0


class BoardConfig(BaseModel):
    board_id: INT_GT_0
    base_url: HttpUrl
    board_name: SAFE_STR
