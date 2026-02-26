import psycopg2
import psycopg2.extras
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from config.neon_config import get_db_connection
from utils.timezone_utils import get_fecha_actual
from models.usuario_habitacion_model import UsuarioHabitacion

class UsuarioHabitacionController:

    def create_usuario_habitacion(self, usuario_habitacion: UsuarioHabitacion): #---
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            fecha_actual = get_fecha_actual()

            query = """
                INSERT INTO usuario_habitacion (
                    id_usuario,
                    id_habitacion,
                    id_reserva,
                    date_check_in,
                    date_check_out,
                    estado,
                    date_created,
                    date_updated
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id_uxh;
            """
            values = (
                usuario_habitacion.id_usuario,
                usuario_habitacion.id_habitacion,
                usuario_habitacion.id_reserva,
                usuario_habitacion.date_check_in,
                usuario_habitacion.date_check_out,
                usuario_habitacion.estado,
                fecha_actual,
                fecha_actual
            )

            cursor.execute(query, values)
            new_id = cursor.fetchone()[0]
            conn.commit()

            return {
                "success": True,
                "message": "Usuario asignado a la habitación correctamente.",
                "id_uxh": new_id
            }

        except Exception as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al crear usuario-habitación: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_usuarios_habitaciones(self): #---
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            cursor.execute("""
                SELECT *
                FROM usuario_habitacion
            """)

            data = cursor.fetchall()

            if not data:
                raise HTTPException(status_code=404, detail="No hay registros usuario-habitación.")

            return {
                "success": True,
                "data": jsonable_encoder(data)
            }

        except Exception as err:
            raise HTTPException(status_code=500, detail=f"Error al obtener registros: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_usuario_habitacion_by_id(self, id_uxh: int): #---
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            cursor.execute("""
                SELECT *
                FROM usuario_habitacion
                WHERE id_uxh = %s
            """, (id_uxh,))

            data = cursor.fetchone()

            if not data:
                raise HTTPException(status_code=404, detail="Registro usuario-habitación no encontrado.")

            return {
                "success": True,
                "data": jsonable_encoder(data)
            }

        except Exception as err:
            raise HTTPException(status_code=500, detail=f"Error al obtener registro: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()