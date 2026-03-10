import psycopg2
from psycopg2 import Error as PsycopgError
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from config.db_config import get_db_connection


class RolesController:

    # ================= LISTAR ROLES =================
    def list_roles(self):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT DISTINCT rol
                FROM seguridad.usuarios
                ORDER BY rol
            """)

            rows = cursor.fetchall()

            roles = [r[0] for r in rows]

            return jsonable_encoder(roles)

        except PsycopgError:
            raise HTTPException(status_code=500, detail="Error consultando roles")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    # ================= LISTAR USUARIOS =================
    def list_users(self):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT id_usuario, nombre, email, rol, estado
                FROM seguridad.usuarios
                ORDER BY id_usuario ASC
            """)

            rows = cursor.fetchall()

            users = []

            for r in rows:
                users.append({
                    "id_usuario": r[0],
                    "nombre": r[1],
                    "email": r[2],
                    "rol": r[3],
                    "estado": r[4]
                })

            return jsonable_encoder(users)

        except PsycopgError:
            raise HTTPException(status_code=500, detail="Error consultando usuarios")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    # ================= CAMBIAR ROL =================
    def change_role(self, user_id: int, new_role: str):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE seguridad.usuarios
                SET rol = %s
                WHERE id_usuario = %s
                RETURNING id_usuario, nombre, email, rol, estado
            """, (new_role, user_id))

            row = cursor.fetchone()

            if not row:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")

            conn.commit()

            return jsonable_encoder({
                "id_usuario": row[0],
                "nombre": row[1],
                "email": row[2],
                "rol": row[3],
                "estado": row[4]
            })

        except PsycopgError:
            conn.rollback()
            raise HTTPException(status_code=400, detail="Error cambiando rol")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    # ================= DESACTIVAR USUARIO =================
    def delete_user(self, user_id: int):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE seguridad.usuarios
                SET estado = false
                WHERE id_usuario = %s
            """, (user_id,))

            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")

            conn.commit()

            return {"resultado": "Usuario desactivado"}

        except PsycopgError:
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error eliminando usuario")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    # ================= ACTIVAR / DESACTIVAR =================
    def toggle_user_status(self, user_id: int):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT estado
                FROM seguridad.usuarios
                WHERE id_usuario = %s
            """, (user_id,))

            user = cursor.fetchone()

            if not user:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")

            nuevo_estado = not user[0]

            cursor.execute("""
                UPDATE seguridad.usuarios
                SET estado = %s
                WHERE id_usuario = %s
            """, (nuevo_estado, user_id))

            conn.commit()

            return {
                "resultado": "Estado actualizado",
                "nuevo_estado": nuevo_estado
            }

        except PsycopgError:
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error cambiando estado")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()