import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from config.neon_config import get_db_connection
from utils.timezone_utils import get_fecha_actual
from models.modulo_rol_model import ModuloRol

class ModuloRolController:
    #
    def create_modulo_rol(self, modulo_rol: ModuloRol):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=psycopg2)
            fecha_actual = get_fecha_actual()

            query = """
                INSERT INTO modulo_rol (
                    id_modulo,
                    id_rol,
                    estado,
                    date_created,
                    date_updated
                )
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id_mxr;
            """
            values = (
                modulo_rol.id_modulo,
                modulo_rol.id_rol,
                modulo_rol.estado,
                fecha_actual,
                fecha_actual
            )

            cursor.execute(query, values)
            new_id = cursor.fetchone()["id_mxr"]
            conn.commit()

            return {
                "success": True,
                "message": "Relación módulo-rol creada correctamente.",
                "id_mxr": new_id
            }

        except Exception as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al crear relación: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    #
    def get_modulos_roles(self):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=psycopg2)

            cursor.execute("""SELECT * FROM modulo_rol""")

            data = cursor.fetchall()

            if not data:
                raise HTTPException(status_code=404, detail="No hay relaciones registradas.")

            return {
                "success": True,
                "data": jsonable_encoder(data)
            }

        except Exception as err:
            raise HTTPException(status_code=500, detail=f"Error al obtener relaciones: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    #
    def get_modulo_rol_by_id(self, id_mxr: int):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=psycopg2)

            cursor.execute("""
                SELECT *
                FROM modulo_rol
                WHERE id_mxr = %s
            """, (id_mxr,))

            data = cursor.fetchone()

            if not data:
                raise HTTPException(status_code=404, detail="Relación no encontrada.")

            return {
                "success": True,
                "data": jsonable_encoder(data)
            }

        except Exception as err:
            raise HTTPException(status_code=500, detail=f"Error al obtener relación: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    #
    def get_modulos_by_rol(self, id_rol: int):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=psycopg2)

            cursor.execute("""
                SELECT 
                    m.id_modulo,
                    m.nombre,
                    m.ruta
                FROM modulo_rol mr
                INNER JOIN modulo m 
                    ON mr.id_modulo = m.id_modulo
                WHERE mr.id_rol = %s
                AND mr.estado = TRUE
                AND m.estado = TRUE
            """, (id_rol,))

            data = cursor.fetchall()

            if not data:
                raise HTTPException(status_code=404, detail="Este rol no tiene módulos asignados.")

            return {
                "success": True,
                "data": jsonable_encoder(data)
            }

        except Exception as err:
            raise HTTPException(status_code=500, detail=f"Error al obtener módulos del rol: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()