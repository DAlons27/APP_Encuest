# Conexion a la base datos

import psycopg

class UserConnection():
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
        #Lo usare para visualizar la informacio de registro del usuario(s), pero tambien puede servir para mostrar las encuestas activas
        with self.conn.cursor() as cur:
            data = cur.execute("""
                SELECT * FROM "user"
                               """)
            return data.fetchall()
        
    def read_one(self, id_usuario):
        with self.conn.cursor() as cur:
            data = cur.execute("""
                SELECT * FROM "user" WHERE id_usuario = %s
                               """, (id_usuario,))
            #modificacando a return data.fetchall() obtengo todos los registros asociados al id... Tambien cambiar la sentencia
            return data.fetchone()
       
    def write(self, data):
        #Registro del usuario
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO "user"(id_usuario, name, lastname, age, email, password) VALUES(%(id_usuario)s, %(name)s, %(lastname)s, %(age)s, %(email)s, %(password)s)
                        """, data)
            # Sentencia sql, inserto nuevos datos en la tablas indicadas, data es un diccionario
            self.conn.commit()

    def authenticate_user(self, id_usuario: str, password: str):
        #Autenticacion del usuario para el login con JWT
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT * FROM "user" WHERE id_usuario = %s AND password = %s
            """, (id_usuario, password))
            return cur.fetchone()

    def __def__(self):
        # destructor

        self.conn.close()
