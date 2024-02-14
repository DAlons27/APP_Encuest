from fastapi import FastAPI, HTTPException, Depends, APIRouter
from model.user_connection import UserConnection
from schema.user_schema import UserSchema, EncuestaCreateSchema, RespuestaSchema
from auth.auth import login_for_access_token, decode_token, router as auth_router
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
router = APIRouter() 
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

# VERIFICADO x2
# Usare este para el login de un usuario    
@app.post("/api/login", response_model=dict)
async def login(email: str, password: str, token: str = Depends(login_for_access_token)):
    return {"token": token}

# VERIFICADO x2
app.include_router(auth_router, prefix="/api", tags=["token"])

# VERIFICADO x2
# Ruta protegida para obtener el perfil del usuario con el token
@app.get("/api/user/profile")
def get_user_profile(token: str = Depends(oauth2_scheme)):
    decoded_token = decode_token(token)
    user_email = decoded_token.get("sub")
    
    # Aquí puedes utilizar el email para obtener la información del usuario desde la base de datos
    # Puedes usar la conexión a la base de datos o el método que prefieras
    user_data = conn.get_user_by_email(user_email)
    
    # Luego, puedes devolver la información del usuario
    return {"email": user_email, "user_data": user_data}

# VERIFICADO X2
# Usare este para listar todos los formularios asociados a un usuario
@app.get("/api/user/encuestas", response_model=list)
def get_user_profile(token: str = Depends(oauth2_scheme)):
    decoded_token = decode_token(token)
    user_email = decoded_token.get("sub")
    # Obtener encuestas asociadas al usuario
    encuestas = conn.get_user_encuestas(user_email) 
    #encuestas = conn.get_user_encuestas(user["email"])  
    return encuestas

# VERIFICADO X2
# Responder encuesta
@app.post("/api/user/encuestas/responder")
def responder_encuesta(respuestas: RespuestaSchema, token: str = Depends(oauth2_scheme)):
    decoded_token = decode_token(token)
    id_usuario = decoded_token.get("sub")

    for respuesta in respuestas.respuestas:
        id_pregunta = respuesta["id_pregunta"]
        id_opcion = respuesta["id_opcion"]
        conn.reply_encuesta(id_usuario, id_pregunta, id_opcion)

    return {"message": "Respuestas registradas exitosamente"}

# VERIFICADO x2
# Usar este para REGISTRAR una encuesta con preguntas y opciones
@app.post("/api/user/crear/encuestas")
def create_encuesta(encuesta_data: EncuestaCreateSchema, token: str = Depends(oauth2_scheme)):
    decoded_token = decode_token(token)
    user_email = decoded_token.get("sub")

    # Crear la encuesta, preguntas y opciones usando la conexión a la base de datos
    conn.create_encuesta(user_email, encuesta_data.titulo, encuesta_data.descripcion, encuesta_data.fecha_fin, encuesta_data.preguntas)

    return {"message": "Encuesta creada exitosamente"}

# VERIFICADO x2
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

# VERIFICADO x2
# Usare este para REGISTRAR un usuario
@app.post("/api/insert")
def insert(user_data:UserSchema):
    data = user_data.model_dump()
    conn.write(data)
    return {"message": "Usuario registrado exitosamente"}

# VERIFICADO x2
# Ruta protegida para obtener todas las encuestas
@app.get("/api/encuestas")
def get_all_encuestas():
    encuestas = conn.get_all_encuestas()
    return encuestas






# FALTA MODIFICAR LA RUTA Y VERIFICARLA
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

# FALTA MODIFICAR LA RUTA Y VERIFICARLA
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

# FALTA MODIFICAR LA RUTA Y VERIFICARLA
# Ruta para obtner todos las encuestas realizadas a detalle
# Opcional
@app.get("/api/encuestas/detalle")
def get_encuestas_realizadas_detalladas():
    # Obtener todas las encuestas con detalles
    encuestas_detalladas = conn.obtener_encuestas_detalladas()

    return encuestas_detalladas