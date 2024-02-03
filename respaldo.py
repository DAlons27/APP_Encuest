from fastapi import FastAPI
from model.user_connection import UserConnection
from schema.user_schema import UserSchema

app = FastAPI()
conn = UserConnection()

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
    #Use el return conn.readone(id) para devolver la informacion pero es mejor dar salida como dict, puede usarse despues para el front...En el return conn.read_all(id) podria devolverme todas las encuestas creadas por el usuario (id) pero debo modificar tambien en user_connectio.py la funcion def read_one, deberia ser return data.fetchall() y cambiar la sentencia sql
    return dictionary

# Usare este para REGISTRAR un usuario
@app.post("/api/insert")
def insert(user_data:UserSchema):
    data = user_data.model_dump()
    #data.pop("nombre del dato"), esto me permite no pasar un dato por mas que este en mi estructura (schema),  podria usarse para el id que se autogenere pero en este caso el usuario lo debe ingresar ademas es llave primaria
    conn.write(data)


# Creare un endpoint para iniciar sesion con id_usuario, password, email...como verificacion usare JWT (Json Web Token) para la autenticacion de usuarios y asi poder acceder a las encuestas creadas por el usuario en especifico y tambien para el registro de las respuestas de las encuestas creadas por el usuario en especifico (POST) , todo esto debe ser verificado con la base de datos.
    
#Ya cree el esquema y el modelo para el login, ahora debo crear el endpoint para el login
    
#@app.post("/api/login")
#def login(user_data:UserLogin):
#    data = user_data.model_dump()

