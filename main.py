from fastapi import FastAPI
from model.user_connection import UserConnection
from schema.user_schema import UserSchema

app = FastAPI()
conn = UserConnection()

@app.get("/")
def root():
    #me lista todo los usuarios
    items = []
    for data in conn.read_all():
        dictionary = {}
        dictionary["id"] = data[0]
        dictionary["name"] = data[1]
        dictionary["lastname"] = data[2]
        dictionary["age"] = data[3]
        dictionary["email"] = data[4]
        dictionary["password"] = data[5]
        items.append(dictionary)
    return items

@app.get("/api/user/{id}")
#me lista un unico usuario con su informacion
def get_one(id:str):
    dictionary = {}
    data = conn.read_one(id)
    dictionary["id"] = data[0]
    dictionary["name"] = data[1]
    dictionary["lastname"] = data[2]
    dictionary["age"] = data[3]
    dictionary["email"] = data[4]
    dictionary["password"] = data[5]
    #Use el return conn.readone(id) para devolver la informacion pero es mejor dar salida como dict, puede usarse despues para el front...En el return conn.read_all(id) podria devolverme todas las encuestas creadas por el usuario (id) pero debo modificar tambien en user_connectio.py la funcion def read_one, deberia ser return data.fetchall() y cambiar la sentencia sql
    return dictionary

@app.post("/api/insert")
def insert(user_data:UserSchema):
    data = user_data.dict()
    #data.pop("nombre del dato")
    #esto me permite no pasar un dato por mas que este en mi estructura (schema),  podria usarse para el id que se autogenere pero en este caso el usuario lo debe ingresar ademas es llave primaria
    conn.write(data)