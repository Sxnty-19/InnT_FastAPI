import psycopg2
import psycopg2.extras
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from config.neon_config import get_db_connection
from utils.timezone_utils import get_fecha_actual
from models.modulo_model import Modulo

class ModuloController:

    def create_modulo(self, modulo: Modulo): #---
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            fecha_actual = get_fecha_actual()

            query = """
                INSERT INTO modulo (
                    nombre,
                    ruta,
                    descripcion,
                    estado,
                    date_created,
                    date_updated
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id_modulo;
            """
            values = (
                modulo.nombre,
                modulo.ruta,
                modulo.descripcion,
                modulo.estado,
                fecha_actual,
                fecha_actual
            )

            cursor.execute(query, values)
            new_id = cursor.fetchone()[0]
            conn.commit()

            return {
                "success": True,
                "message": "Módulo creado correctamente.",
                "id_modulo": new_id
            }

        except Exception as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al crear módulo: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_modulos(self): #---
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            cursor.execute("""
                SELECT *
                FROM modulo
            """)

            data = cursor.fetchall()

            if not data:
                raise HTTPException(status_code=404, detail="No hay módulos registrados.")

            return {
                "success": True,
                "data": jsonable_encoder(data)
            }

        except Exception as err:
            raise HTTPException(status_code=500, detail=f"Error al obtener módulos: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_modulo_by_id(self, id_modulo: int): #---
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(
                cursor_factory=psycopg2.extras.RealDictCursor
            )

            cursor.execute("""
                SELECT *
                FROM modulo
                WHERE id_modulo = %s
            """, (id_modulo,))

            data = cursor.fetchone()

            if not data:
                raise HTTPException(status_code=404, detail="Módulo no encontrado.")

            return {
                "success": True,
                "data": jsonable_encoder(data)
            }

        except Exception as err:
            raise HTTPException(status_code=500, detail=f"Error al obtener módulo: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()