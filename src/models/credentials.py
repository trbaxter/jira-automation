from pydantic import BaseModel

from src.constants.shared import SAFE_STR


class Credentials(BaseModel):
    email: SAFE_STR
    token: SAFE_STR
