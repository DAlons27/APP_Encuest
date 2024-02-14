# Conexion a la base datos
from typing import List
from schema.user_schema import PreguntaSchema
import psycopg
from datetime import datetime

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

    # VERIFICADO x2
    # Autenticar usuario
    def authenticate_user(self, email: str, password: str):
        with self.conn:
            cur = self.conn.cursor()
            cur.execute("""
                SELECT * FROM "user" WHERE email = %s AND password = %s
            """, (email, password))
            # Fetch the result
            result = cur.fetchone()

            # Convertir la tupla de resultado a un diccionario manualmente
            if result:
                user_dict = {
                    "id_usuario": result[0],
                    "name": result[1],
                    "lastname": result[2],
                    "age": result[3],
                    "email": result[4],
                    "password": result[5]
                }
                return user_dict
            else:
                return None

    # VERIFICADO x2
    # Lo usare para visualizar la informacion de todos los usuarios
    def read_all(self):
        with self.conn.cursor() as cur:
            data = cur.execute("""
                SELECT * FROM "user"
                               """)
            return data.fetchall()

    # VERIFICADO x2
    # Lo usare para visualizar la informacion de un usuario en especifico segun un email
    def read_one(self, email):

        with self.conn.cursor() as cur:
            data = cur.execute("""
                SELECT * FROM "user" WHERE email = %s
                               """, (email,))
            #modificacando a return data.fetchall() obtengo todos los registros asociados al id... Tambien cambiar la sentencia
            return data.fetchone()

    # VERIFICADO x2
    # REGISTRO DEL USUARIO       
    def write(self, data):
        
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO "user"(name, lastname, age, email, password) VALUES(%(name)s, %(lastname)s, %(age)s, %(email)s, %(password)s)
                        """, data)
            self.conn.commit()

    # VERIFICADO x2
    # Obtener un usuario por email
    def get_user_by_email(self, email: str):
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT * FROM "user" WHERE email = %s
            """, (email,))
            return cur.fetchone()

    # VERIFICADO x2
    # Obtener las encuestas asociadas a un usuario solo el campo titulo y descripcion
    def get_user_encuestas(self, email: str):
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT e.titulo, e.descripcion
                FROM encuestas e
                JOIN "user" u ON e.id_usuario = u.id_usuario
                WHERE u.email = %s
            """, (email,))
            encuestas = cur.fetchall()
        return encuestas
    
    # VERIFICADO x2
    # Función para obtener el id_usuario por correo electrónico
    def get_user_id_by_email(self, email: str):
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT id_usuario FROM "user" WHERE email = %s
            """, (email,))
            result = cur.fetchone()

        if result:
            return result[0]
        else:
            return None

    # VERIFICADO x2
    # Obtener todas las encuestas: titulo y descripcion
    def get_all_encuestas(self):
        #Obtener todas las encuestas, solo el campo titulo y descripcion
        # TODAS LAS ENCUESTAS
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT titulo, descripcion FROM "encuestas" 
            """)
            encuestas = cur.fetchall()
        return encuestas
    
    # VERIFICADO x2
    # Crear una nueva encuesta con preguntas y opciones
    def create_encuesta(self, email: str, titulo: str, descripcion: str, fecha_fin: str, preguntas: List[PreguntaSchema]):
                      
        fecha_creacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Obtener el id_usuario asociado al correo electrónico
        id_usuario = self.get_user_id_by_email(email)

        # Crear una nueva encuesta
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO encuestas(id_usuario, titulo, descripcion, fecha_creacion, fecha_fin)
                VALUES (%s, %s, %s, %s, %s) RETURNING id_encuestas
            """, (id_usuario ,titulo, descripcion, fecha_creacion, fecha_fin))
            id_encuesta = cur.fetchone()[0]                  

            # Insertar preguntas y opciones asociadas
            for pregunta_data in preguntas:
                cur.execute("""
                    INSERT INTO preguntas(id_encuestas, preguntas)
                    VALUES (%s, %s) RETURNING id_preguntas
                """, (id_encuesta, pregunta_data.pregunta))
                id_pregunta = cur.fetchone()[0]

                for opcion_data in pregunta_data.opciones:
                    cur.execute("""
                        INSERT INTO opciones(id_preguntas, opciones)
                        VALUES (%s, %s) 
                    """, (id_pregunta, opcion_data.opcion_texto))

            self.conn.commit() 

    # VERIFICADO X2
    # Responder a una encuesta
    def reply_encuesta(self, email:str, id_pregunta: int, id_opcion: int):

        id_usuario = self.get_user_id_by_email(email)

        with self.conn.cursor() as cur:

        # Insertar la respuesta en la tabla respuestas
            cur.execute("""
                INSERT INTO respuestas(id_opciones, id_usuario)
                VALUES (%s, %s)
            """, (id_opcion, id_usuario))

            self.conn.commit() 





    # Obtener las encuestas realizadas por el usuario con detalles de sus respuestas
    def get_user_encuestas_detalladas(self, id_usuario: int):
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT 
                        encuestas.titulo, 
                        encuestas.descripcion, 
                        preguntas.preguntas, 
                        opciones.opciones, 
                        respuestas.id_opciones
                FROM encuestas
                LEFT JOIN preguntas ON encuestas.id_encuestas = preguntas.id_encuestas
                LEFT JOIN opciones ON preguntas.id_preguntas = opciones.id_preguntas
                LEFT JOIN respuestas ON opciones.id_opciones = respuestas.id_opciones AND respuestas.id_usuario = %s
                WHERE encuestas.id_usuario = %s
                ORDER BY preguntas.id_preguntas ASC;
            """, (id_usuario, id_usuario))
            encuestas_detalladas = cur.fetchall()

        return encuestas_detalladas

    # Igual que get_user_encuestas_detalladas, pero la respuesta sale en formato de lista
    def get_detalle_encuesta(self, id_usuario: int):

        id_usuario = self.get_user_id_by_email(id_usuario)

        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT
                    encuestas.titulo,
                    encuestas.descripcion,
                    preguntas.id_preguntas,
                    preguntas.preguntas,
                    ARRAY_AGG(opciones.opciones) AS opciones,
                    ARRAY_AGG(CASE WHEN respuestas.id_opciones IS NOT NULL THEN opciones.opciones ELSE NULL END) AS respuestas
                FROM "user"
                LEFT JOIN encuestas ON "user".id_usuario = encuestas.id_usuario
                LEFT JOIN preguntas ON encuestas.id_encuestas = preguntas.id_encuestas
                LEFT JOIN opciones ON preguntas.id_preguntas = opciones.id_preguntas
                LEFT JOIN respuestas ON opciones.id_opciones = respuestas.id_opciones AND "user".id_usuario = respuestas.id_usuario
                WHERE
                    ("user".id_usuario = %s AND respuestas.id_opciones IS NULL) OR
                    ("user".id_usuario = %s AND respuestas.id_opciones IS NOT NULL) OR
                    ("user".id_usuario != %s AND respuestas.id_opciones IS NOT NULL)
                GROUP BY
                    encuestas.titulo, encuestas.descripcion, preguntas.id_preguntas, preguntas.preguntas
                ORDER BY
                    preguntas.id_preguntas ASC;
            """, (id_usuario, id_usuario, id_usuario))
            prueba = cur.fetchall()

        # Procesar el resultado para formatearlo
        formatted_result = []
        for row in prueba:
            formatted_row = list(row)
            # Convertir el conjunto de opciones en un solo valor
            formatted_row[4] = formatted_row[4] if formatted_row[4] is not None else []
            # Convertir la respuesta en un solo valor
            formatted_row[5] = formatted_row[5] if formatted_row[5] is not None else []
            formatted_result.append(tuple(formatted_row))
        #print(formatted_result)   
        #formatted_result.sort(key=lambda x: x[2] if x[2] is not None else float('inf')) 
        return formatted_result

    # Me permite obtner todos las encuestas realizadas a detalle
    # OPCIONAL 
    def obtener_encuestas_detalladas(self):
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT
                    encuestas.titulo,
                    encuestas.descripcion,
                    preguntas.id_preguntas,
                    preguntas.preguntas,
                    ARRAY_AGG(opciones.opciones) AS opciones,
                    ARRAY_AGG(CASE WHEN respuestas.id_opciones IS NOT NULL THEN opciones.opciones ELSE NULL END) AS respuestas
                FROM encuestas
                LEFT JOIN preguntas ON encuestas.id_encuestas = preguntas.id_encuestas
                LEFT JOIN opciones ON preguntas.id_preguntas = opciones.id_preguntas
                LEFT JOIN respuestas ON opciones.id_opciones = respuestas.id_opciones
                GROUP BY encuestas.titulo, encuestas.descripcion, preguntas.id_preguntas, preguntas.preguntas
                ORDER BY preguntas.id_preguntas ASC;
            """)
            encuestas = cur.fetchall()

        # Procesar el resultado para formatearlo
        formatted_result = []
        for row in encuestas:
            formatted_row = list(row)
            # Convertir el conjunto de opciones en un solo valor
            formatted_row[4] = formatted_row[4] if formatted_row[4] is not None else []
            # Convertir la respuesta en un solo valor
            formatted_row[5] = formatted_row[5] if formatted_row[5] is not None else []
            formatted_result.append(tuple(formatted_row))

        return formatted_result      
    

    def __def__(self):
        # esta funcion se ejecuta al finalizar el programa o al cerrar la conexion con la base de datos 

        self.conn.close()