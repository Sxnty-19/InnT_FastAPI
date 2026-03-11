import psycopg2
from fastapi import HTTPException
from config.neon_config import get_db_connection
from utils.pass_utils import hash_password , verify_password
from utils.timezone_utils import get_fecha_actual
from utils.auth_utils import crear_token
from models.usuario_model import Usuario

class AuthController:
    #
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
    #
    def login_user(self, username: str, password: str):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT 
                    u.id_usuario,
                    u.password,
                    u.primer_nombre,
                    u.segundo_nombre,
                    u.primer_apellido,
                    u.segundo_apellido,
                    r.id_rol,
                    r.nombre
                FROM usuario u
                INNER JOIN rol r ON u.id_rol = r.id_rol
                WHERE u.username = %s AND u.estado = true
            """, (username,))

            user = cursor.fetchone()

            if not user:
                raise HTTPException(status_code=404, detail="Usuario o Contraseña Incorrectos")

            id_usuario = user[0]
            password_db = user[1]

            primer_nombre = user[2]
            segundo_nombre = user[3] or ""
            primer_apellido = user[4]
            segundo_apellido = user[5] or ""

            id_rol = user[6]
            nombre_rol = user[7]

            if not verify_password(password, password_db):
                raise HTTPException(status_code=401, detail="Usuario o Contraseña Incorrectos")

            nombre_completo = f"{primer_nombre} {segundo_nombre} {primer_apellido} {segundo_apellido}".strip()

            payload = {
                "id_usuario": id_usuario,
                "id_rol": id_rol
            }

            token = crear_token(payload)

            return {
                "success": True,
                "access_token": token,
                "token_type": "bearer",
                "user": {
                    "nombre": nombre_completo,
                    "id_usuario": id_usuario,   
                    "rol": nombre_rol,
                    "id_rol": id_rol
                }
            }

        except psycopg2.Error as err:
            raise HTTPException(status_code=500, detail=f"Error en la base de datos: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
            
    def login_azure(self, correo: str):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT 
                    u.id_usuario,
                    u.primer_nombre,
                    u.segundo_nombre,
                    u.primer_apellido,
                    u.segundo_apellido,
                    r.id_rol,
                    r.nombre
                FROM usuario u
                INNER JOIN rol r ON u.id_rol = r.id_rol
                WHERE u.correo = %s AND u.estado = true
            """, (correo,))

            user = cursor.fetchone()

            if not user:
                raise HTTPException(status_code=404, detail="Usuario no registrado")

            id_usuario = user[0]

            primer_nombre = user[1]
            segundo_nombre = user[2] or ""
            primer_apellido = user[3]
            segundo_apellido = user[4] or ""

            id_rol = user[5]
            nombre_rol = user[6]

            nombre_completo = f"{primer_nombre} {segundo_nombre} {primer_apellido} {segundo_apellido}".strip()

            payload = {
                "id_usuario": id_usuario,
                "id_rol": id_rol
            }

            token = crear_token(payload)

            return {
                "success": True,
                "access_token": token,
                "token_type": "bearer",
                "user": {
                    "nombre": nombre_completo,
                    "id_usuario": id_usuario,
                    "rol": nombre_rol,
                    "id_rol": id_rol
                }
            }

        except psycopg2.Error as err:
            raise HTTPException(status_code=500, detail=f"Error en la base de datos: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()