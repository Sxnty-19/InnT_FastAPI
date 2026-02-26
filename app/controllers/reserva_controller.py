import psycopg2
import psycopg2.extras
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from config.neon_config import get_db_connection
from utils.timezone_utils import get_fecha_actual
from models.reserva_model import Reserva

class ReservaController:

    def create_reserva(self, reserva: Reserva): #---
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            fecha_actual = get_fecha_actual()

            query = """
                INSERT INTO reserva (
                    id_usuario,
                    date_start,
                    date_end,
                    total,
                    estado,
                    date_created,
                    date_updated
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id_reserva;
            """
            values = (
                reserva.id_usuario,
                reserva.date_start,
                reserva.date_end,
                reserva.total,
                reserva.estado,
                fecha_actual,
                fecha_actual
            )

            cursor.execute(query, values)
            new_id = cursor.fetchone()[0]
            conn.commit()

            return {
                "success": True,
                "message": "Reserva creada correctamente.",
                "id_reserva": new_id
            }

        except Exception as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al crear reserva: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_reservas(self): #---
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            cursor.execute("""
                SELECT *
                FROM reserva
            """)

            data = cursor.fetchall()

            if not data:
                raise HTTPException(status_code=404, detail="No hay reservas registradas.")

            return {
                "success": True,
                "data": jsonable_encoder(data)
            }

        except Exception as err:
            raise HTTPException(status_code=500,detail=f"Error al obtener reservas: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_reserva_by_id(self, id_reserva: int): #---
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            cursor.execute("""
                SELECT *
                FROM reserva
                WHERE id_reserva = %s
            """, (id_reserva,))

            data = cursor.fetchone()

            if not data:
                raise HTTPException(status_code=404, detail="Reserva no encontrada.")

            return {
                "success": True,
                "data": jsonable_encoder(data)
            }

        except Exception as err:
            raise HTTPException(status_code=500, detail=f"Error al obtener reserva: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()