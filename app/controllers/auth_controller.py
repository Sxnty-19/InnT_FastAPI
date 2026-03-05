from fastapi import HTTPException
from config.neon_config import get_db_connection
from utils.pass_utils import hash_password
from utils.timezone_utils import get_fecha_actual
from models.usuario_model import Usuario
import psycopg2

class AuthController:

    def register_user(self, usuario: Usuario):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            fecha_actual = get_fecha_actual()
            id_rol = 3

            if usuario.correo:
                cursor.execute(
                    "SELECT id_usuario FROM usuario WHERE correo = %s",(usuario.correo,)
                )
                if cursor.fetchone():
                    raise HTTPException(status_code=400, detail="El correo ya está registrado")

            cursor.execute(
                "SELECT id_usuario FROM usuario WHERE username = %s", (usuario.username,)
            )
            if cursor.fetchone():
                raise HTTPException(status_code=400, detail="El nombre de usuario ya está en uso")

            hashed_pw = hash_password(usuario.password)

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
                RETURNING id_usuario
            """
            values = (
                id_rol,
                usuario.primer_nombre,
                usuario.segundo_nombre,
                usuario.primer_apellido,
                usuario.segundo_apellido,
                usuario.telefono,
                usuario.correo,
                usuario.username,
                hashed_pw,
                usuario.estado,
                fecha_actual,
                fecha_actual
            )
            cursor.execute(query, values)
            new_id = cursor.fetchone()[0]
            conn.commit()

            return {
                "success": True,
                "message": "Usuario registrado exitosamente",
                "id_usuario": new_id
            }

        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error en la base de datos: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()