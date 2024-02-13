from fastapi import FastAPI, HTTPException, Depends
from model.user_connection import UserConnection
from schema.user_schema import UserSchema, EncuestaCreateSchema, RespuestaSchema
from auth.auth import login_for_access_token
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
conn = UserConnection()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
global_token = None

# Configuración de CORS
origins = [
    "http://localhost",
    "http://localhost:8000",  # Agrega aquí las URL de tus clientes front-end permitidos
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#VERIFICADO
# Usare este para el login de un usuario    
@app.post("/api/login", response_model=dict)
async def login(email: str, password: str, token: str = Depends(login_for_access_token)):
    return {"token": token}

#VERIFICADO
# Usare este para MOSTRAR un usuario en especifico segun su email
@app.get("/api/user/{email}")
def get_one(email:str):
    dictionary = {}
    data = conn.read_one(email)
    dictionary["id_usuario"] = data[0]
    dictionary["name"] = data[1]
    dictionary["lastname"] = data[2]
    dictionary["age"] = data[3]
    dictionary["email"] = data[4]
    dictionary["password"] = data[5]

    return dictionary

#VERIFICADO
# Usare esto para MOSTRAR todos los usuarios registrados.
@app.get("/")
def root():

    items = []
    for data in conn.read_all():    
        dictionary = {}
        dictionary["id_usuario"] = data[0]
        dictionary["name"] = data[1]
        dictionary["lastname"] = data[2]
        dictionary["age"] = data[3]
        dictionary["email"] = data[4]
        dictionary["password"] = data[5]
        items.append(dictionary)
    return items

#VERIFICADO
# Usare este para REGISTRAR un usuario
@app.post("/api/insert")
def insert(user_data:UserSchema):
    data = user_data.model_dump()
    conn.write(data)
    return {"message": "Usuario registrado exitosamente"}

#VERIFICADO
# Ruta protegida para obtener todas las encuestas
@app.get("/api/encuestas")
def get_all_encuestas():
    encuestas = conn.get_all_encuestas()
    return encuestas

# Usare este para listar todos los formularios asociados a un usuario
@app.get("/api/user/{email}/encuestas")
def get_user_encuestas(id_usuario: int):
    # Verificar si el usuario existe
    user_data = conn.read_one(id_usuario)
    if not user_data:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Obtener encuestas asociadas al id_usuario
    encuestas = conn.get_user_encuestas(id_usuario)

    return encuestas

# Usar este para REGISTRAR una encuesta con preguntas y opciones
@app.post("/api/user/{id_usuario}/encuestas")
def create_encuesta(id_usuario: int, encuesta_data: EncuestaCreateSchema):
    # Verificar si el usuario existe
    user_data = conn.read_one(id_usuario)
    if not user_data:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Crear la encuesta, preguntas y opciones usando la conexión a la base de datos
    conn.create_encuesta(id_usuario, encuesta_data.titulo, encuesta_data.descripcion, encuesta_data.fecha_fin, encuesta_data.preguntas)

    return {"message": "Encuesta creada exitosamente"}

# Usar este para MOSTRAR las encuestas realizadas por un usuario con detalles
@app.get("/api/user/{id_usuario}/detalle_encuestas")
def get_user_encuestas_realizadas_detalladas(id_usuario: int):
    # Verificar si el usuario existe
    user_data = conn.read_one(id_usuario)
    if not user_data:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Obtener las encuestas realizadas por el usuario con detalles
    encuestas_detalladas = conn.get_user_encuestas_detalladas(id_usuario)

    return encuestas_detalladas

# Igual que get_user_encuestas_detalladas, pero la respuesta sale en formato de lista
@app.get("/api/user/{id_usuario}/prueba")
def prueba_encuesta(id_usuario: int):
    
    # Verificar si el usuario existe
    user_data = conn.read_one(id_usuario)
    if not user_data:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Obtener las encuestas realizadas por el usuario con detalles
    encuestas_detalladas = conn.prueba(id_usuario)

    return encuestas_detalladas

# Ruta para respoder a una encuesta  
@app.post("/api/user/{id_usuario}/encuestas/{id_encuesta}/responder")
def responder_encuesta(id_usuario: int, id_encuesta: int, respuestas: RespuestaSchema):
    for respuesta in respuestas.respuestas:
        id_pregunta = respuesta["id_pregunta"]
        id_opcion = respuesta["id_opcion"]
        conn.responder_encuesta(id_usuario, id_encuesta, id_pregunta, id_opcion)

    return {"message": "Respuestas registradas exitosamente"}

# Ruta para obtner todos las encuestas realizadas a detalle
# Opcional
@app.get("/api/encuestas/detalle")
def get_encuestas_realizadas_detalladas():
    # Obtener todas las encuestas con detalles
    encuestas_detalladas = conn.obtener_encuestas_detalladas()

    return encuestas_detalladas