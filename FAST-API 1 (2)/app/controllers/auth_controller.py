from fastapi import HTTPException
from psycopg2 import Error as PsycopgError
from config.db_config import get_db_connection
from security import verify_password, create_access_token


class AuthController:

    def login(self, email: str, password: str):
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT id_usuario, email, password_hash, rol
                FROM seguridad.usuarios
                WHERE email=%s AND estado=true
            """, (email,))

            user = cursor.fetchone()

            # 🔎 DEBUG
            print("USER DB:", user)
            print("PASSWORD INPUT:", password)

            if not user:
                raise HTTPException(401, "Credenciales inválidas")

            if not verify_password(password, user[2]):
                raise HTTPException(401, "Credenciales inválidas")

            token = create_access_token({
                "sub": str(user[0]),
                "email": user[1],
                "rol": user[3]
            })

            return {
                "access_token": token,
                "token_type": "bearer"
            }

        except PsycopgError as e:
            raise HTTPException(500, detail=str(e))

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()