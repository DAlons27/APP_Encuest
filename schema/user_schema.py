from pydantic import BaseModel
from typing import Optional

class UserSchema(BaseModel):
    id_usuario: int
    name: str
    lastname: str
    age: str
    email: str
    password: str

class UserLogin(BaseModel):
    id_usuario: int
    password: str