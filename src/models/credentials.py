from pydantic import BaseModel, Field

from src.customtypes.shared import NonEmptyStr


class Credentials(BaseModel):
    email: NonEmptyStr
    token: NonEmptyStr = Field(repr=False)
