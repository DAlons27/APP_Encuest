from pydantic import BaseModel
from typing import List, Dict

class UserSchema(BaseModel):
    name: str
    lastname: str
    age: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class OpcionSchema(BaseModel):
    opcion_texto: str

class PreguntaSchema(BaseModel):
    pregunta: str
    opciones: List[OpcionSchema]

class EncuestaCreateSchema(BaseModel):
    titulo: str
    descripcion: str
    fecha_fin: str
    preguntas: List[PreguntaSchema]
    
class RespuestaSchema(BaseModel):
    respuestas: List[Dict[str, int]]