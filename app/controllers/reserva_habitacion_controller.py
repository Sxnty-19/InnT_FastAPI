import psycopg2
import psycopg2.extras
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from config.neon_config import get_db_connection
from utils.timezone_utils import get_fecha_actual
from models.reserva_habitacion_model import ReservaHabitacion

class ReservaHabitacionController:

    def create_reserva_habitacion(self, reserva_habitacion: ReservaHabitacion): #---
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            fecha_actual = get_fecha_actual()

            query = """
                INSERT INTO reserva_habitacion (
                    id_reserva,
                    id_habitacion,
                    estado,
                    date_created,
                    date_updated
                )
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id_rxh;
            """
            values = (
                reserva_habitacion.id_reserva,
                reserva_habitacion.id_habitacion,
                reserva_habitacion.estado,
                fecha_actual,
                fecha_actual
            )

            cursor.execute(query, values)
            new_id = cursor.fetchone()[0]
            conn.commit()

            return {
                "success": True,
                "message": "Habitación asignada a la reserva correctamente.",
                "id_rxh": new_id
            }

        except Exception as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al crear relación reserva-habitación: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_reservas_habitaciones(self): #---
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            cursor.execute("""
                SELECT *
                FROM reserva_habitacion
            """)

            data = cursor.fetchall()

            if not data:
                raise HTTPException(status_code=404, detail="No hay relaciones reserva-habitación registradas.")

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

    def get_reserva_habitacion_by_id(self, id_rxh: int): #---
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            cursor.execute("""
                SELECT *
                FROM reserva_habitacion
                WHERE id_rxh = %s
            """, (id_rxh,))

            data = cursor.fetchone()

            if not data:
                raise HTTPException(status_code=404, detail="Relación reserva-habitación no encontrada.")

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