from fastapi import HTTPException
from psycopg2 import Error as PsycopgError
from fastapi.encoders import jsonable_encoder
from config.db_config import get_db_connection
from models.persona_model import PersonaCreate


class PersonasController:

    # ================= CREATE =================
    def crear_persona(self, data: PersonaCreate):
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO violencia.personas
                (documento, id_genero, id_nacionalidad, edad)
                VALUES (%s, %s, %s, %s)
                RETURNING id_persona
            """, (
                data.documento,
                data.id_genero,
                data.id_nacionalidad,
                data.edad
            ))

            nuevo_id = cursor.fetchone()[0]
            conn.commit()

            return {
                "resultado": "Persona creada correctamente",
                "id_persona": nuevo_id
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
    def listar_personas(self):
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT id_persona, documento, id_genero, id_nacionalidad, edad
                FROM violencia.personas
                WHERE estado=true
            """)

            result = cursor.fetchall()

            personas = []
            for row in result:
                personas.append({
                    "id_persona": row[0],
                    "documento": row[1],
                    "id_genero": row[2],
                    "id_nacionalidad": row[3],
                    "edad": row[4]
                })

            return {"resultado": jsonable_encoder(personas)}

        except PsycopgError as e:
            raise HTTPException(500, detail=str(e))

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    # ================= UPDATE =================
    def actualizar_persona(self, persona_id: int, data: PersonaCreate):
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE violencia.personas
                SET documento=%s,
                    id_genero=%s,
                    id_nacionalidad=%s,
                    edad=%s
                WHERE id_persona=%s
            """, (
                data.documento,
                data.id_genero,
                data.id_nacionalidad,
                data.edad,
                persona_id
            ))

            if cursor.rowcount == 0:
                raise HTTPException(404, "Persona no encontrada")

            conn.commit()

            return {"resultado": "Persona actualizada correctamente"}

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
    def eliminar_persona(self, persona_id: int):
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE violencia.personas
                SET estado=false
                WHERE id_persona=%s
            """, (persona_id,))

            if cursor.rowcount == 0:
                raise HTTPException(404, "Persona no encontrada")

            conn.commit()

            return {"resultado": "Persona eliminada correctamente"}

        except PsycopgError as e:
            if conn:
                conn.rollback()
            raise HTTPException(500, detail=str(e))

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()