import psycopg2
from psycopg2 import Error as PsycopgError
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from config.db_config import get_db_connection
from models.user_model import UserCreate
from security import hash_password


class UserController:

    # ================= CREATE =================
    def create_user(self, user: UserCreate):
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT id_usuario FROM seguridad.usuarios
                WHERE email=%s OR cedula=%s OR usuario=%s
            """, (user.email, user.cedula, user.usuario))

            if cursor.fetchone():
                raise HTTPException(409, "Usuario ya existe")

            # 🔐 HASH PASSWORD
            hashed_password = hash_password(user.contrasena)

            cursor.execute("""
                INSERT INTO seguridad.usuarios
                (nombre, usuario, cedula, edad, email, password_hash, rol)
                VALUES (%s,%s,%s,%s,%s,%s,%s)
                RETURNING id_usuario
            """, (
                user.nombre,
                user.usuario,
                user.cedula,
                user.edad,
                user.email,
                hashed_password,  # 👈 ahora va hasheada
                user.rol
            ))

            nuevo_id = cursor.fetchone()[0]
            conn.commit()

            return {
                "resultado": "Usuario creado",
                "id": nuevo_id
            }

        except Exception as e:
            if conn:
                conn.rollback()
            raise HTTPException(500, str(e))

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    # ================= GET ONE =================
    def get_user(self, user_id: int):
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT id_usuario, nombre, usuario, cedula, edad, email, rol
                FROM seguridad.usuarios
                WHERE id_usuario=%s AND estado=true
            """, (user_id,))

            row = cursor.fetchone()

            if not row:
                raise HTTPException(404, "Usuario no encontrado")

            return jsonable_encoder({
                "id": row[0],
                "nombre": row[1],
                "usuario": row[2],
                "cedula": row[3],
                "edad": row[4],
                "email": row[5],
                "rol": row[6]
            })

        except PsycopgError as e:
            raise HTTPException(500, detail=str(e))

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    # ================= GET ALL =================
    def get_users(self):
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT id_usuario, nombre, usuario, cedula, edad, email, rol
                FROM seguridad.usuarios
                WHERE estado=true
            """)

            result = cursor.fetchall()

            payload = []
            for row in result:
                payload.append({
                    "id": row[0],
                    "nombre": row[1],
                    "usuario": row[2],
                    "cedula": row[3],
                    "edad": row[4],
                    "email": row[5],
                    "rol": row[6]
                })

            return {"resultado": jsonable_encoder(payload)}

        except PsycopgError as e:
            raise HTTPException(500, detail=str(e))

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    # ================= DELETE (LÓGICO) =================
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
                raise HTTPException(404, "Usuario no encontrado")

            conn.commit()

            return {"resultado": "Usuario eliminado correctamente"}

        except PsycopgError as e:
            if conn:
                conn.rollback()
            raise HTTPException(500, detail=str(e))

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

            # ================= UPDATE =================
    def update_user(self, user_id: int, user: UserCreate):
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # 🔎 Obtener password actual
            cursor.execute(
                "SELECT password_hash  FROM seguridad.usuarios WHERE id_usuario=%s",
                (user_id,)
            )
            current_user = cursor.fetchone()

            if not current_user:
                raise HTTPException(404, "Usuario no encontrado")

            # 🔐 Si la contraseña ya viene hasheada, no re-hashear
            if user.contrasena.startswith("$2b$"):
                hashed_password = user.contrasena
            else:
                hashed_password = hash_password(user.contrasena)

            cursor.execute("""
                UPDATE seguridad.usuarios
                SET nombre=%s,
                    usuario=%s,
                    cedula=%s,
                    edad=%s,
                    email=%s,
                    password_hash=%s,
                    rol=%s
                WHERE id_usuario=%s
            """, (
                user.nombre,
                user.usuario,
                user.cedula,
                user.edad,
                user.email,
                hashed_password,
                user.rol,
                user_id
            ))

            conn.commit()

            return {"resultado": "Usuario actualizado correctamente"}

        except PsycopgError as e:
            if conn:
                conn.rollback()
            raise HTTPException(500, detail=str(e))

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()