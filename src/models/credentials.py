from pydantic import BaseModel, constr

class Credentials(BaseModel):
    email: constr(strip_whitespace=True, min_length=1)
    token: constr(strip_whitespace=True, min_length=1)