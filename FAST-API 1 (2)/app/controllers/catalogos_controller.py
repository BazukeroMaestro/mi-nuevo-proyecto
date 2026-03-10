from fastapi import HTTPException
from psycopg2 import Error as PsycopgError
from config.db_config import get_db_connection
from models.catalogos_model import CatalogoCreate


class CatalogosController:

    # ================= MUNICIPIOS =================

    def crear_municipio(self, data: CatalogoCreate):
        return self._crear("violencia.municipios", "nombre_normalizado", data.nombre)

    def listar_municipios(self):
        return self._listar("violencia.municipios")

    def actualizar_municipio(self, item_id: int, data: CatalogoCreate):
        return self._actualizar("violencia.municipios", "id_municipio",
                                "nombre_normalizado", item_id, data.nombre)

    def eliminar_municipio(self, item_id: int):
        return self._eliminar("violencia.municipios", "id_municipio", item_id)


    # ================= EPS =================

    def crear_eps(self, data: CatalogoCreate):
        return self._crear("violencia.eps", "nombre_normalizado", data.nombre)

    def listar_eps(self):
        return self._listar("violencia.eps")

    def actualizar_eps(self, item_id: int, data: CatalogoCreate):
        return self._actualizar("violencia.eps", "id_eps",
                                "nombre_normalizado", item_id, data.nombre)

    def eliminar_eps(self, item_id: int):
        return self._eliminar("violencia.eps", "id_eps", item_id)


    # ================= ESCOLARIDADES =================

    def crear_escolaridad(self, data: CatalogoCreate):
        return self._crear("violencia.escolaridades", "nivel_normalizado", data.nombre)

    def listar_escolaridades(self):
        return self._listar("violencia.escolaridades")

    def actualizar_escolaridad(self, item_id: int, data: CatalogoCreate):
        return self._actualizar("violencia.escolaridades", "id_escolaridad",
                                "nivel_normalizado", item_id, data.nombre)

    def eliminar_escolaridad(self, item_id: int):
        return self._eliminar("violencia.escolaridades", "id_escolaridad", item_id)


    # ================= OCUPACIONES =================

    def crear_ocupacion(self, data: CatalogoCreate):
        return self._crear("violencia.ocupaciones", "ocupacion_normalizada", data.nombre)

    def listar_ocupaciones(self):
        return self._listar("violencia.ocupaciones")

    def actualizar_ocupacion(self, item_id: int, data: CatalogoCreate):
        return self._actualizar("violencia.ocupaciones", "id_ocupacion",
                                "ocupacion_normalizada", item_id, data.nombre)

    def eliminar_ocupacion(self, item_id: int):
        return self._eliminar("violencia.ocupaciones", "id_ocupacion", item_id)


    # ================= MÉTODOS PRIVADOS =================

    def _crear(self, tabla, campo, valor):
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                f"INSERT INTO {tabla} ({campo}) VALUES (%s)",
                (valor,)
            )

            conn.commit()
            return {"resultado": "Registro creado correctamente"}

        except PsycopgError as e:
            if conn:
                conn.rollback()
            raise HTTPException(500, detail=str(e))

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def _listar(self, tabla):
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                f"SELECT * FROM {tabla} WHERE estado=true"
            )

            result = cursor.fetchall()
            return {"resultado": result}

        except PsycopgError as e:
            raise HTTPException(500, detail=str(e))

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def _actualizar(self, tabla, id_field, campo, item_id, valor):
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                f"UPDATE {tabla} SET {campo}=%s WHERE {id_field}=%s",
                (valor, item_id)
            )

            if cursor.rowcount == 0:
                raise HTTPException(404, "Registro no encontrado")

            conn.commit()
            return {"resultado": "Registro actualizado correctamente"}

        except PsycopgError as e:
            if conn:
                conn.rollback()
            raise HTTPException(500, detail=str(e))

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def _eliminar(self, tabla, id_field, item_id):
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                f"UPDATE {tabla} SET estado=false WHERE {id_field}=%s",
                (item_id,)
            )

            if cursor.rowcount == 0:
                raise HTTPException(404, "Registro no encontrado")

            conn.commit()
            return {"resultado": "Registro eliminado correctamente"}

        except PsycopgError as e:
            if conn:
                conn.rollback()
            raise HTTPException(500, detail=str(e))

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
        # ================= GENEROS =================

    def crear_genero(self, data):
        return self._crear("violencia.generos", "genero_normalizado", data.nombre)

    def listar_generos(self):
        return self._listar("violencia.generos")

    def actualizar_genero(self, item_id, data):
        return self._actualizar("violencia.generos", "id_genero",
                                "genero_normalizado", item_id, data.nombre)

    def eliminar_genero(self, item_id):
        return self._eliminar("violencia.generos", "id_genero", item_id)


    # ================= NACIONALIDADES =================

    def crear_nacionalidad(self, data):
        return self._crear("violencia.nacionalidades", "nacionalidad_normalizada", data.nombre)

    def listar_nacionalidades(self):
        return self._listar("violencia.nacionalidades")

    def actualizar_nacionalidad(self, item_id, data):
        return self._actualizar("violencia.nacionalidades", "id_nacionalidad",
                                "nacionalidad_normalizada", item_id, data.nombre)

    def eliminar_nacionalidad(self, item_id):
        return self._eliminar("violencia.nacionalidades", "id_nacionalidad", item_id)
    
        # ================= TIPOS VIOLENCIA =================

    def crear_tipo_violencia(self, data):
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO violencia.tipos_violencia
                (codigo, descripcion)
                VALUES (%s, %s)
            """, (data.codigo, data.descripcion))

            conn.commit()
            return {"resultado": "Tipo de violencia creado"}

        except PsycopgError as e:
            if conn:
                conn.rollback()
            raise HTTPException(500, detail=str(e))
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()


    def listar_tipos_violencia(self):
        return self._listar("violencia.tipos_violencia")


    def actualizar_tipo_violencia(self, item_id, data):
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE violencia.tipos_violencia
                SET codigo=%s,
                    descripcion=%s
                WHERE id_tipo_violencia=%s
            """, (data.codigo, data.descripcion, item_id))

            if cursor.rowcount == 0:
                raise HTTPException(404, "No encontrado")

            conn.commit()
            return {"resultado": "Actualizado"}

        except PsycopgError as e:
            if conn:
                conn.rollback()
            raise HTTPException(500, detail=str(e))
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()


    def eliminar_tipo_violencia(self, item_id):
        return self._eliminar(
            "violencia.tipos_violencia",
            "id_tipo_violencia",
            item_id
        )
    
        # ================= CARACTERIZACIONES =================

    def crear_caracterizacion(self, data):
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO violencia.caracterizaciones
                (caracterizacion_normalizada,
                 es_psicologica, es_fisica, es_sexual,
                 es_economica, es_patrimonial, es_ciberacoso)
                VALUES (%s,%s,%s,%s,%s,%s,%s)
            """, (
                data.caracterizacion_normalizada,
                data.es_psicologica,
                data.es_fisica,
                data.es_sexual,
                data.es_economica,
                data.es_patrimonial,
                data.es_ciberacoso
            ))

            conn.commit()
            return {"resultado": "Caracterización creada"}

        except PsycopgError as e:
            if conn:
                conn.rollback()
            raise HTTPException(500, detail=str(e))
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()


    def listar_caracterizaciones(self):
        return self._listar("violencia.caracterizaciones")


    def actualizar_caracterizacion(self, item_id, data):
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE violencia.caracterizaciones
                SET caracterizacion_normalizada=%s,
                    es_psicologica=%s,
                    es_fisica=%s,
                    es_sexual=%s,
                    es_economica=%s,
                    es_patrimonial=%s,
                    es_ciberacoso=%s
                WHERE id_caracterizacion=%s
            """, (
                data.caracterizacion_normalizada,
                data.es_psicologica,
                data.es_fisica,
                data.es_sexual,
                data.es_economica,
                data.es_patrimonial,
                data.es_ciberacoso,
                item_id
            ))

            if cursor.rowcount == 0:
                raise HTTPException(404, "No encontrado")

            conn.commit()
            return {"resultado": "Actualizado"}

        except PsycopgError as e:
            if conn:
                conn.rollback()
            raise HTTPException(500, detail=str(e))
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()


    def eliminar_caracterizacion(self, item_id):
        return self._eliminar(
            "violencia.caracterizaciones",
            "id_caracterizacion",
            item_id
        )