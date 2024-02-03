from fastapi import FastAPI, HTTPException
from model.user_connection import UserConnection
from schema.user_schema import UserSchema, UserLogin
from auth.auth import authenticate_user
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()
conn = UserConnection()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
global_token = None

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