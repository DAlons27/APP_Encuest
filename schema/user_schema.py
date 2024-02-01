from pydantic import BaseModel
from typing import Optional

class UserSchema(BaseModel):
    id: int
    name: str
    lastname: str
    age: str
    email: str
    password: str