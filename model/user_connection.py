# Conexion a la base datos

import psycopg

class UserConnection():
    # clase para la conexion con la base de datos
    conn = None
    # atributo
    
    def __init__(self):
        # constructor
        try:
            self.conn = psycopg.connect("dbname=fastapi_test user=postgres password=Nuevo2024 host=localhost port=5432")
            # conexion con la base de datos
            
        except psycopg.OperationalError as err:
            print(err)
            self.conn.close()
            # cierra la base de datos en caso de error

    def read_all(self):
        #Lo usare para visualizar la informacion de todos los usuarios
        with self.conn.cursor() as cur:
            data = cur.execute("""
                SELECT * FROM "user"
                               """)
            return data.fetchall()
        
    def read_one(self, id_usuario):
        #Lo usare para visualizar la informacion de un usuario en especifico
        # MOSTRAR UN USUARIO
        with self.conn.cursor() as cur:
            data = cur.execute("""
                SELECT * FROM "user" WHERE id_usuario = %s
                               """, (id_usuario,))
            #modificacando a return data.fetchall() obtengo todos los registros asociados al id... Tambien cambiar la sentencia
            return data.fetchone()
       
    def write(self, data):
        #REGISTRO DEL USUARIO
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO "user"(id_usuario, name, lastname, age, email, password) VALUES(%(id_usuario)s, %(name)s, %(lastname)s, %(age)s, %(email)s, %(password)s)
                        """, data)
            # Sentencia sql, inserto nuevos datos en la tablas indicadas, data es un diccionario
            self.conn.commit()

    def authenticate_user(self, id_usuario: str, password: str):
        #Autenticacion del usuario para el login con JWT
        # LOGIN DEL USUARIO
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT * FROM "user" WHERE id_usuario = %s AND password = %s
            """, (id_usuario, password))
            return cur.fetchone()

    def get_user_encuestas(self, id_usuario: int):
        #Obtener las encuestas asociadas a un usuario, solo el campo titulo
        # MIS ENCUESTAS
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT titulo FROM encuestas WHERE id_usuario = %s
            """, (id_usuario,))
            encuestas = cur.fetchall()
        return encuestas
    
    def get_all_encuestas(self):
        #Obtener todas las encuestas, solo el campo titulo
        # TODAS LAS ENCUESTAS
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT titulo FROM "encuestas"
            """)
            encuestas = cur.fetchall()
        return encuestas

    def __def__(self):
        # esta funcion se ejecuta al finalizar el programa o al cerrar la conexion con la base de datos 

        self.conn.close()