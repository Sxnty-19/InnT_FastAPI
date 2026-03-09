import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from config.neon_config import get_db_connection
from utils.timezone_utils import get_fecha_actual
from models.habitacion_model import Habitacion

class HabitacionController:
    #
    def create_habitacion(self, habitacion: Habitacion):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            fecha_actual = get_fecha_actual()

            query = """
                INSERT INTO habitacion (
                    id_thabitacion,
                    numero,
                    limpieza,
                    estado,
                    date_created,
                    date_updated
                ) VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id_habitacion
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
            new_id = cursor.fetchone()["id_habitacion"]
            conn.commit()

            return {
                "success": True,
                "message": "Habitación creada correctamente.",
                "id_habitacion": new_id
            }

        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al crear habitación: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    #
    def get_habitaciones(self):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute("SELECT * FROM habitacion")

            data = cursor.fetchall()

            if not data:
                raise HTTPException(status_code=404, detail="No hay habitaciones registradas.")

            return {
                "success": True,
                "data": jsonable_encoder(data)
            }

        except psycopg2.Error as err:
            raise HTTPException(status_code=500, detail=f"Error al obtener habitaciones: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    #
    def get_habitacion_by_id(self, id_habitacion: int):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute("""
                SELECT * FROM habitacion
                WHERE id_habitacion = %s
            """, (id_habitacion,))

            data = cursor.fetchone()

            if not data:
                raise HTTPException(status_code=404, detail="Habitación no encontrada.")

            return {
                "success": True,
                "data": jsonable_encoder(data)
            }

        except psycopg2.Error as err:
            raise HTTPException(status_code=500, detail=f"Error al obtener habitación: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    #
    def actualizar_limpieza_por_id(self, id_habitacion: int):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            fecha_actual = get_fecha_actual()

            cursor.execute("""
                SELECT limpieza FROM habitacion 
                WHERE id_habitacion = %s
            """,(id_habitacion,))

            habitacion = cursor.fetchone()

            if not habitacion:
                raise HTTPException(status_code=404, detail=f"Habitación con ID {id_habitacion} no encontrada.")

            nueva_limpieza = not habitacion["limpieza"]

            query = """
                UPDATE habitacion
                SET limpieza = %s,
                    date_updated = %s
                WHERE id_habitacion = %s
            """

            cursor.execute(query, (nueva_limpieza, fecha_actual, id_habitacion))
            conn.commit()

            return {
                "success": True,
                "message": "Estado de limpieza actualizado."
            }

        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al actualizar limpieza: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    #
    def get_habitaciones_disponibles(self, date_start: str, date_end: str):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute("""
                SELECT h.*
                FROM habitacion h
                WHERE h.estado = TRUE
                AND NOT EXISTS (
                    SELECT 1
                    FROM reserva_habitacion rh
                    JOIN reserva r ON rh.id_reserva = r.id_reserva
                    WHERE rh.id_habitacion = h.id_habitacion
                    AND r.estado = TRUE
                    AND r.date_start < %s
                    AND r.date_end > %s
                )
            """, (date_end, date_start))

            data = cursor.fetchall()

            return {
                "success": True,
                "data": jsonable_encoder(data)
            }

        except psycopg2.Error as err:
            raise HTTPException(status_code=500, detail=f"Error al obtener habitaciones disponibles: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()