from pydantic import BaseModel

from src.constants.field_types import SAFE_STR


class Credentials(BaseModel):
    email: SAFE_STR
    token: SAFE_STR
