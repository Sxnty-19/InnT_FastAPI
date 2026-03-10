import psycopg2
import psycopg2.extras
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from config.neon_config import get_db_connection
from utils.timezone_utils import get_fecha_actual
from utils.pass_utils import hash_password, verify_password
from models.usuario_model import Usuario

class UsuarioController:

    def create_usuario(self, usuario: Usuario): #---
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            fecha_actual = get_fecha_actual()

            query = """
                INSERT INTO usuario (
                    id_rol,
                    primer_nombre,
                    segundo_nombre,
                    primer_apellido,
                    segundo_apellido,
                    telefono,
                    correo,
                    username,
                    password,
                    estado,
                    date_created,
                    date_updated
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id_usuario;
            """
            values = (
                usuario.id_rol,
                usuario.primer_nombre,
                usuario.segundo_nombre,
                usuario.primer_apellido,
                usuario.segundo_apellido,
                usuario.telefono,
                usuario.correo,
                usuario.username,
                usuario.password,
                usuario.estado,
                fecha_actual,
                fecha_actual
            )

            cursor.execute(query, values)
            new_id = cursor.fetchone()[0]
            conn.commit()

            return {
                "success": True,
                "message": "Usuario creado correctamente.",
                "id_usuario": new_id
            }

        except Exception as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al crear usuario: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_usuarios(self): #---
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            cursor.execute("""
                SELECT *
                FROM usuario
            """)

            data = cursor.fetchall()

            if not data:
                raise HTTPException(status_code=404, detail="No hay usuarios registrados.")

            return {
                "success": True,
                "data": jsonable_encoder(data)
            }

        except Exception as err:
            raise HTTPException(status_code=500, detail=f"Error al obtener usuarios: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_usuario_by_id(self, id_usuario: int): #---
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            cursor.execute("""
                SELECT *
                FROM usuario
                WHERE id_usuario = %s
            """, (id_usuario,))

            data = cursor.fetchone()

            if not data:
                raise HTTPException(
                    status_code=404,
                    detail="Usuario no encontrado."
                )

            return {
                "success": True,
                "data": jsonable_encoder(data)
            }

        except Exception as err:
            raise HTTPException( status_code=500, detail=f"Error al obtener usuario: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_usuario(self, payload: dict):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            id_usuario = payload["id_usuario"]


            cursor.execute("""
                SELECT *
                FROM usuario
                WHERE id_usuario = %s
            """, (id_usuario,))

            data = cursor.fetchone()

            if not data:
                raise HTTPException(
                    status_code=404,
                    detail="Usuario no encontrado."
                )

            return {
                "success": True,
                "data": jsonable_encoder(data)
            }

        except Exception as err:
            raise HTTPException( status_code=500, detail=f"Error al obtener usuario: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    def update_usuario(self, data: dict, payload: dict):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            id_usuario = payload["id_usuario"]

            campos_permitidos = {
                "primer_nombre",
                "segundo_nombre",
                "primer_apellido",
                "segundo_apellido",
                "telefono"
            }

            # Filtrar solo los campos permitidos
            data = {k: v for k, v in data.items() if k in campos_permitidos}

            if not data:
                raise HTTPException(status_code=400, detail="No hay campos válidos para actualizar")

            campos = ", ".join([f"{key} = %s" for key in data.keys()])
            valores = list(data.values())

            query = f"""
                UPDATE usuario 
                SET {campos}, date_updated = %s
                WHERE id_usuario = %s
            """

            valores.append(get_fecha_actual())
            valores.append(id_usuario)

            cursor.execute(query, valores)
            conn.commit()

            return {
                "success": True,
                "message": "Usuario actualizado correctamente"
            }

        except psycopg2.Error as err:
            raise HTTPException(status_code=500, detail=f"Error al actualizar usuario: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()