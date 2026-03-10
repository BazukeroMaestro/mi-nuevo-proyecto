from fastapi import HTTPException
from psycopg2 import Error as PsycopgError
from fastapi.encoders import jsonable_encoder
from config.db_config import get_db_connection
from models.atencion_model import AtencionCreate


class AtencionesController:

    # ================= CREATE =================
    def crear_atencion(self, data: AtencionCreate):
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO violencia.atenciones
                (id_persona, id_municipio, id_eps, id_escolaridad,
                 id_ocupacion, id_tipo_violencia, id_caracterizacion,
                 fecha_atencion, parentesco, observaciones)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                RETURNING id_atencion
            """, (
                data.id_persona,
                data.id_municipio,
                data.id_eps,
                data.id_escolaridad,
                data.id_ocupacion,
                data.id_tipo_violencia,
                data.id_caracterizacion,
                data.fecha_atencion,
                data.parentesco,
                data.observaciones
            ))

            nuevo_id = cursor.fetchone()[0]
            conn.commit()

            return {
                "resultado": "Atención creada correctamente",
                "id_atencion": nuevo_id
            }

        except PsycopgError as e:
            if conn:
                conn.rollback()
            raise HTTPException(500, detail=str(e))

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    # ================= LISTAR =================
    def listar_atenciones(self):
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM violencia.atenciones
                WHERE estado=true
            """)

            result = cursor.fetchall()

            return {"resultado": jsonable_encoder(result)}

        except PsycopgError as e:
            raise HTTPException(500, detail=str(e))

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    # ================= UPDATE =================
    def actualizar_atencion(self, atencion_id: int, data: AtencionCreate):
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE violencia.atenciones
                SET id_persona=%s,
                    id_municipio=%s,
                    id_eps=%s,
                    id_escolaridad=%s,
                    id_ocupacion=%s,
                    id_tipo_violencia=%s,
                    id_caracterizacion=%s,
                    fecha_atencion=%s,
                    parentesco=%s,
                    observaciones=%s
                WHERE id_atencion=%s
            """, (
                data.id_persona,
                data.id_municipio,
                data.id_eps,
                data.id_escolaridad,
                data.id_ocupacion,
                data.id_tipo_violencia,
                data.id_caracterizacion,
                data.fecha_atencion,
                data.parentesco,
                data.observaciones,
                atencion_id
            ))

            if cursor.rowcount == 0:
                raise HTTPException(404, "Atención no encontrada")

            conn.commit()

            return {"resultado": "Atención actualizada correctamente"}

        except PsycopgError as e:
            if conn:
                conn.rollback()
            raise HTTPException(500, detail=str(e))

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    # ================= DELETE LÓGICO =================
    def eliminar_atencion(self, atencion_id: int):
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE violencia.atenciones
                SET estado=false
                WHERE id_atencion=%s
            """, (atencion_id,))

            if cursor.rowcount == 0:
                raise HTTPException(404, "Atención no encontrada")

            conn.commit()

            return {"resultado": "Atención eliminada correctamente"}

        except PsycopgError as e:
            if conn:
                conn.rollback()
            raise HTTPException(500, detail=str(e))

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()