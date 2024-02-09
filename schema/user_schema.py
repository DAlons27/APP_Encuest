from pydantic import BaseModel
from typing import List

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

# Servira para la creacion de encuestas
class OpcionSchema(BaseModel):
    opcion_texto: str
class PreguntaSchema(BaseModel):
    pregunta: str
    opciones: List[OpcionSchema]
class EncuestaCreateSchema(BaseModel):
    titulo: str
    descripcion: str
    fecha_creacion: str
    fecha_fin: str
    preguntas: List[PreguntaSchema]
