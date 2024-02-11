from fastapi import FastAPI, HTTPException
from model.user_connection import UserConnection
from schema.user_schema import UserSchema, UserLogin, EncuestaCreateSchema
from auth.auth import authenticate_user
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

# Usare este para LOGEAR un usuario    
@app.post("/api/login", response_model=dict)
def login(user_login: UserLogin):
    global global_token

    try:
        user = authenticate_user(conn, user_login.id_usuario, user_login.password)

        if user:
        # Almacena el token en la variable global
            global_token = user.get("token")
            return {"message": "Usuario autenticado exitosamente", "token": global_token}

        return user  # Esto incluirá el token si la autenticación fue exitosa
    except HTTPException as e:
        return {"error": e.detail}

# Usare este para MOSTRAR un usuario en especifico
@app.get("/api/user/{id_usuario}")
def get_one(id_usuario:str):
    dictionary = {}
    data = conn.read_one(id_usuario)
    dictionary["id_usuario"] = data[0]
    dictionary["name"] = data[1]
    dictionary["lastname"] = data[2]
    dictionary["age"] = data[3]
    dictionary["email"] = data[4]
    dictionary["password"] = data[5]

    return dictionary

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

# Usare este para REGISTRAR un usuario
@app.post("/api/insert")
def insert(user_data:UserSchema):
    data = user_data.model_dump()
    #data.pop("nombre del dato"), esto me permite no pasar un dato por mas que este en mi estructura (schema),  podria usarse para el id que se autogenere pero en este caso el usuario lo debe ingresar ademas es llave primaria
    conn.write(data)
    return {"message": "Usuario registrado exitosamente"}

# Ruta protegida para obtener todas las encuestas
@app.get("/api/encuestas")
def get_all_encuestas():
    encuestas = conn.get_all_encuestas()
    return encuestas

# Usare este para listar todos los formularios asociados a un usuario
@app.get("/api/user/{id_usuario}/encuestas")
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

# Ruta de prueba
@app.get("/api/user/{id_usuario}/prueba")
def prueba_encuesta(id_usuario: int):
    # Verificar si el usuario existe
    user_data = conn.read_one(id_usuario)
    if not user_data:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Obtener las encuestas realizadas por el usuario con detalles
    encuestas_detalladas = conn.prueba(id_usuario)

    return encuestas_detalladas