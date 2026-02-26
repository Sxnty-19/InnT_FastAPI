import psycopg2
import psycopg2.extras
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from config.neon_config import get_db_connection
from utils.timezone_utils import get_fecha_actual
from models.solicitud_model import Solicitud

class SolicitudController:

    def create_solicitud(self, solicitud: Solicitud): #---
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            fecha_actual = get_fecha_actual()

            query = """
                INSERT INTO solicitud (
                    id_usuario,
                    id_habitacion,
                    descripcion,
                    prioridad,
                    estado,
                    date_created,
                    date_updated
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id_solicitud;
            """
            values = (
                solicitud.id_usuario,
                solicitud.id_habitacion,
                solicitud.descripcion,
                solicitud.prioridad,
                solicitud.estado,
                fecha_actual,
                fecha_actual
            )

            cursor.execute(query, values)
            new_id = cursor.fetchone()[0]
            conn.commit()

            return {
                "success": True,
                "message": "Solicitud creada correctamente.",
                "id_solicitud": new_id
            }

        except Exception as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al crear solicitud: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_solicitudes(self): #---
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            cursor.execute("""
                SELECT *
                FROM solicitud
            """)

            data = cursor.fetchall()

            if not data:
                raise HTTPException(status_code=404, detail="No hay solicitudes registradas.")

            return {
                "success": True,
                "data": jsonable_encoder(data)
            }

        except Exception as err:
            raise HTTPException(status_code=500, detail=f"Error al obtener solicitudes: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_solicitud_by_id(self, id_solicitud: int): #---
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            cursor.execute("""
                SELECT *
                FROM solicitud
                WHERE id_solicitud = %s
            """, (id_solicitud,))

            data = cursor.fetchone()

            if not data:
                raise HTTPException(status_code=404, detail="Solicitud no encontrada.")

            return {
                "success": True,
                "data": jsonable_encoder(data)
            }

        except Exception as err:
            raise HTTPException(status_code=500, detail=f"Error al obtener solicitud: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()