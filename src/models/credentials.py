from pydantic import BaseModel

from src.fieldtypes.common import SAFE_STR


class Credentials(BaseModel):
    email: SAFE_STR
    token: SAFE_STR
