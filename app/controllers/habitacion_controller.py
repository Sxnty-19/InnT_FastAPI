import psycopg2
import psycopg2.extras
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from config.neon_config import get_db_connection
from utils.timezone_utils import get_fecha_actual
from models.habitacion_model import Habitacion

class HabitacionController:

    def create_habitacion(self, habitacion: Habitacion): #---
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            fecha_actual = get_fecha_actual()

            query = """
                INSERT INTO habitacion (
                    id_thabitacion,
                    numero,
                    limpieza,
                    estado,
                    date_created,
                    date_updated
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id_habitacion;
            """
            values = (
                habitacion.id_thabitacion,
                habitacion.numero,
                habitacion.limpieza,
                habitacion.estado,
                fecha_actual,
                fecha_actual
            )

            cursor.execute(query, values)
            new_id = cursor.fetchone()[0]
            conn.commit()

            return {
                "success": True,
                "message": "Habitación creada correctamente.",
                "id_habitacion": new_id
            }

        except Exception as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al crear habitación: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_habitaciones(self): #---
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            cursor.execute("""
                SELECT *
                FROM habitacion
            """)

            data = cursor.fetchall()

            if not data:
                raise HTTPException(status_code=404, detail="No hay habitaciones registradas.")

            return {
                "success": True,
                "data": jsonable_encoder(data)
            }

        except Exception as err:
            raise HTTPException(status_code=500, detail=f"Error al obtener habitaciones: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_habitacion_by_id(self, id_habitacion: int): #---
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            cursor.execute("""
                SELECT *
                FROM habitacion
                WHERE id_habitacion = %s
            """, (id_habitacion,))

            data = cursor.fetchone()

            if not data:
                raise HTTPException(status_code=404, detail="Habitación no encontrada.")

            return {
                "success": True,
                "data": jsonable_encoder(data)
            }

        except Exception as err:
            raise HTTPException(status_code=500, detail=f"Error al obtener habitación: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()