import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from config.neon_config import get_db_connection
from utils.timezone_utils import get_fecha_actual
from models.documento_model import Documento

class DocumentoController:
    #
    def create_documento(self, documento: Documento):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            fecha_actual = get_fecha_actual()

            query = """
                INSERT INTO documento (
                    id_tdocumento,
                    id_usuario,
                    numero_documento,
                    lugar_expedicion,
                    documento_validado,
                    estado,
                    date_created,
                    date_updated
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id_documento
            """
            values = (
                documento.id_tdocumento,
                documento.id_usuario,
                documento.numero_documento,
                documento.lugar_expedicion,
                documento.documento_validado,
                documento.estado,
                fecha_actual,
                fecha_actual
            )

            cursor.execute(query, values)
            new_id = cursor.fetchone()["id_documento"]
            conn.commit()

            return {
                "success": True,
                "message": "Documento creado correctamente.",
                "id_documento": new_id
            }

        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al crear documento: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    #
    def get_documentos(self):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute("SELECT * FROM documento")

            data = cursor.fetchall()

            if not data:
                raise HTTPException(status_code=404, detail="No hay documentos registrados.")

            return {
                "success": True,
                "data": jsonable_encoder(data)
            }

        except psycopg2.Error as err:
            raise HTTPException(status_code=500, detail=f"Error al obtener documentos: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    #
    def get_documento_by_id(self, id_documento: int):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute("""
                SELECT * FROM documento
                WHERE id_documento = %s
            """, (id_documento,))

            data = cursor.fetchone()

            if not data:
                raise HTTPException(status_code=404, detail="Documento no encontrado.")

            return {
                "success": True,
                "data": jsonable_encoder(data)
            }

        except psycopg2.Error as err:
            raise HTTPException(status_code=500, detail=f"Error al obtener documento: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    #
    def get_documentos_por_usuario(self, id_usuario: int):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute("""
                SELECT
                    d.*,
                    td.nombre AS tipo_documento
                FROM documento d
                JOIN tipo_documento td 
                    ON d.id_tdocumento = td.id_tdocumento
                WHERE d.id_usuario = %s
                AND d.estado = TRUE
            """, (id_usuario,))

            data = cursor.fetchall()

            if not data:
                raise HTTPException(status_code=404, detail="No hay documentos registrados para este usuario.")

            return {
                "success": True,
                "data": jsonable_encoder(data)
            }

        except psycopg2.Error as err:
            raise HTTPException(status_code=500, detail=f"Error al obtener documentos: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    #
    def buscar_usuario_por_documento(self, numero_documento: str):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute("""
                SELECT
                    u.id_usuario,
                    u.primer_nombre,
                    u.segundo_nombre,
                    u.primer_apellido,
                    u.segundo_apellido
                FROM documento d
                INNER JOIN usuario u 
                    ON d.id_usuario = u.id_usuario
                WHERE d.numero_documento = %s
                LIMIT 1
            """, (numero_documento,))

            data = cursor.fetchone()

            if not data:
                raise HTTPException(status_code=404, detail="No se encontró ningún usuario con ese número de documento.")

            return {
                "success": True,
                "message": "Usuario encontrado.",
                "data": jsonable_encoder(data)
            }

        except psycopg2.Error as err:
            raise HTTPException(status_code=500, detail=f"Error al buscar usuario: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()