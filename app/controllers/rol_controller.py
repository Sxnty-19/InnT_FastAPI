import psycopg2
import psycopg2.extras
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from config.neon_config import get_db_connection
from utils.timezone_utils import get_fecha_actual
from models.rol_model import Rol

class RolController:

    def create_rol(self, rol: Rol):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            fecha_actual = get_fecha_actual()

            query = """
                INSERT INTO rol (
                    nombre,
                    descripcion,
                    estado,
                    date_created,
                    date_updated
                )
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id_rol;
            """
            values = (
                rol.nombre,
                rol.descripcion,
                rol.estado,
                fecha_actual,
                fecha_actual
            )

            cursor.execute(query, values)
            new_id = cursor.fetchone()[0]
            conn.commit()

            return {
                "success": True,
                "message": "Rol creado correctamente.",
                "id_rol": new_id
            }

        except Exception as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al crear rol: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_roles(self): #---
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(
                cursor_factory=psycopg2.extras.RealDictCursor
            )

            cursor.execute("""
                SELECT *
                FROM rol
            """)

            data = cursor.fetchall()

            if not data:
                raise HTTPException(status_code=404, detail="No hay roles registrados.")

            return {
                "success": True,
                "data": jsonable_encoder(data)
            }

        except Exception as err:
            raise HTTPException(status_code=500, detail=f"Error al obtener roles: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_rol_by_id(self, id_rol: int): #---
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            cursor.execute("""
                SELECT *
                FROM rol
                WHERE id_rol = %s
            """, (id_rol,))

            data = cursor.fetchone()

            if not data:
                raise HTTPException(
                    status_code=404,
                    detail="Rol no encontrado."
                )

            return {
                "success": True,
                "data": jsonable_encoder(data)
            }

        except Exception as err:
            raise HTTPException(status_code=500, detail=f"Error al obtener rol: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()