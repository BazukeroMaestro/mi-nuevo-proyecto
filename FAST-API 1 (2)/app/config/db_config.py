import psycopg2

def get_db_connection():
    conn = psycopg2.connect(
        host="ep-solitary-scene-aia502e3-pooler.c-4.us-east-1.aws.neon.tech",
        database="neondb",
        user="neondb_owner",
        password="npg_vhU9tJlkYS1r",
        sslmode="require"
    )

    cursor = conn.cursor()
    cursor.execute("SET search_path TO violencia, seguridad;")
    cursor.close()

    return conn
