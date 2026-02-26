import psycopg2
import psycopg2.extras
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from config.neon_config import get_db_connection
from utils.timezone_utils import get_fecha_actual
from models.documento_model import Documento

class DocumentoController:

    def create_documento(self, documento: Documento):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            fecha_actual = get_fecha_actual()

            query = """
                INSERT INTO documento (
                    id_tdocumento,
                    id_usuario,
                    numero_documento,
                    lugar_expedicion,
                    estado,
                    date_created,
                    date_updated
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id_documento;
            """
            values = (
                documento.id_tdocumento,
                documento.id_usuario,
                documento.numero_documento,
                documento.lugar_expedicion,
                documento.estado,
                fecha_actual,
                fecha_actual
            )

            cursor.execute(query, values)
            new_id = cursor.fetchone()[0]
            conn.commit()

            return {
                "success": True,
                "message": "Documento creado correctamente.",
                "id_documento": new_id
            }

        except Exception as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al crear documento: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_documentos(self):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            cursor.execute("""
                SELECT *
                FROM documento
            """)

            data = cursor.fetchall()

            if not data:
                raise HTTPException(status_code=404, detail="No hay documentos registrados.")

            return {
                "success": True,
                "data": jsonable_encoder(data)
            }

        except Exception as err:
            raise HTTPException(status_code=500, detail=f"Error al obtener documentos: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_documento_by_id(self, id_documento: int):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            cursor.execute("""
                SELECT *
                FROM documento
                WHERE id_documento = %s
            """, (id_documento,))

            data = cursor.fetchone()

            if not data:
                raise HTTPException(status_code=404, detail="Documento no encontrado.")

            return {
                "success": True,
                "data": jsonable_encoder(data)
            }

        except Exception as err:
            raise HTTPException(status_code=500, detail=f"Error al obtener documento: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()