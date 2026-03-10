SET search_path TO atencion, public;


CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.actualizado_en = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- ================== CONTROL / SEGURIDAD ===================

CREATE TABLE IF NOT EXISTS usuarios (
  id_usuario        BIGSERIAL PRIMARY KEY,
  nombre            TEXT NOT NULL,
  email             TEXT NOT NULL UNIQUE,
  password_hash     TEXT NOT NULL,
  rol               TEXT NOT NULL CHECK (rol IN ('ADMIN','ANALISTA')),
  estado            BOOLEAN NOT NULL DEFAULT TRUE,
  creado_en         TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  actualizado_en    TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE TRIGGER tg_usuarios_updated
BEFORE UPDATE ON usuarios
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TABLE IF NOT EXISTS permisos (
  id_permiso        BIGSERIAL PRIMARY KEY,
  codigo            TEXT NOT NULL UNIQUE,
  descripcion       TEXT,
  estado            BOOLEAN NOT NULL DEFAULT TRUE,
  creado_en         TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  actualizado_en    TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE TRIGGER tg_permisos_updated
BEFORE UPDATE ON permisos
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TABLE IF NOT EXISTS usuario_permiso (
  id_usuario_permiso  BIGSERIAL PRIMARY KEY,
  id_usuario          BIGINT NOT NULL REFERENCES usuarios(id_usuario),
  id_permiso          BIGINT NOT NULL REFERENCES permisos(id_permiso),
  estado              BOOLEAN NOT NULL DEFAULT TRUE,
  creado_en           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  actualizado_en      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  CONSTRAINT uq_usuario_permiso UNIQUE (id_usuario, id_permiso)
);
CREATE TRIGGER tg_usuario_permiso_updated
BEFORE UPDATE ON usuario_permiso
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

-- ======================== CATÁLOGOS =======================

CREATE TABLE IF NOT EXISTS municipios (
  id_municipio        BIGSERIAL PRIMARY KEY,
  nombre_normalizado  TEXT NOT NULL UNIQUE,
  codigo_dane         TEXT UNIQUE,
  estado              BOOLEAN NOT NULL DEFAULT TRUE,
  creado_en           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  actualizado_en      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE TRIGGER tg_municipios_updated
BEFORE UPDATE ON municipios
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TABLE IF NOT EXISTS eps (
  id_eps              BIGSERIAL PRIMARY KEY,
  nombre_normalizado  TEXT NOT NULL UNIQUE,
  estado              BOOLEAN NOT NULL DEFAULT TRUE,
  creado_en           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  actualizado_en      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE TRIGGER tg_eps_updated
BEFORE UPDATE ON eps
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TABLE IF NOT EXISTS escolaridades (
  id_escolaridad      BIGSERIAL PRIMARY KEY,
  nivel_normalizado   TEXT NOT NULL UNIQUE,
  estado              BOOLEAN NOT NULL DEFAULT TRUE,
  creado_en           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  actualizado_en      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE TRIGGER tg_escolaridades_updated
BEFORE UPDATE ON escolaridades
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TABLE IF NOT EXISTS ocupaciones (
  id_ocupacion          BIGSERIAL PRIMARY KEY,
  ocupacion_normalizada TEXT NOT NULL UNIQUE,
  categoria_ocupacion   TEXT,
  estado                BOOLEAN NOT NULL DEFAULT TRUE,
  creado_en             TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  actualizado_en        TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE TRIGGER tg_ocupaciones_updated
BEFORE UPDATE ON ocupaciones
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TABLE IF NOT EXISTS generos (
  id_genero           BIGSERIAL PRIMARY KEY,
  genero_normalizado  TEXT NOT NULL UNIQUE,
  estado              BOOLEAN NOT NULL DEFAULT TRUE,
  creado_en           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  actualizado_en      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE TRIGGER tg_generos_updated
BEFORE UPDATE ON generos
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TABLE IF NOT EXISTS nacionalidades (
  id_nacionalidad          BIGSERIAL PRIMARY KEY,
  nacionalidad_normalizada TEXT NOT NULL UNIQUE,
  estado                   BOOLEAN NOT NULL DEFAULT TRUE,
  creado_en                TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  actualizado_en           TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE TRIGGER tg_nacionalidades_updated
BEFORE UPDATE ON nacionalidades
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TABLE IF NOT EXISTS tipos_violencia (
  id_tipo_violencia   BIGSERIAL PRIMARY KEY,
  codigo              TEXT NOT NULL UNIQUE,
  descripcion         TEXT,
  estado              BOOLEAN NOT NULL DEFAULT TRUE,
  creado_en           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  actualizado_en      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE TRIGGER tg_tipos_violencia_updated
BEFORE UPDATE ON tipos_violencia
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TABLE IF NOT EXISTS caracterizaciones (
  id_caracterizacion       BIGSERIAL PRIMARY KEY,
  caracterizacion_normalizada TEXT NOT NULL UNIQUE,
  es_psicologica           BOOLEAN NOT NULL DEFAULT FALSE,
  es_fisica                BOOLEAN NOT NULL DEFAULT FALSE,
  es_sexual                BOOLEAN NOT NULL DEFAULT FALSE,
  es_economica             BOOLEAN NOT NULL DEFAULT FALSE,
  es_patrimonial           BOOLEAN NOT NULL DEFAULT FALSE,
  es_ciberacoso            BOOLEAN NOT NULL DEFAULT FALSE,
  estado                   BOOLEAN NOT NULL DEFAULT TRUE,
  creado_en                TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  actualizado_en           TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE TRIGGER tg_caracterizaciones_updated
BEFORE UPDATE ON caracterizaciones
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

-- ======================== ENTIDADES =======================

CREATE TABLE IF NOT EXISTS personas (
  id_persona        BIGSERIAL PRIMARY KEY,
  documento         TEXT UNIQUE,
  id_genero         BIGINT REFERENCES generos(id_genero),
  id_nacionalidad   BIGINT REFERENCES nacionalidades(id_nacionalidad),
  edad              NUMERIC(5,2),
  estado            BOOLEAN NOT NULL DEFAULT TRUE,
  creado_en         TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  actualizado_en    TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE TRIGGER tg_personas_updated
BEFORE UPDATE ON personas
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

-- ===================== TRANSACCIONAL ======================

CREATE TABLE IF NOT EXISTS atenciones (
  id_atencion         BIGSERIAL PRIMARY KEY,
  id_persona          BIGINT NOT NULL REFERENCES personas(id_persona),
  id_municipio        BIGINT REFERENCES municipios(id_municipio),
  id_eps              BIGINT REFERENCES eps(id_eps),
  id_escolaridad      BIGINT REFERENCES escolaridades(id_escolaridad),
  id_ocupacion        BIGINT REFERENCES ocupaciones(id_ocupacion),
  id_tipo_violencia   BIGINT NOT NULL REFERENCES tipos_violencia(id_tipo_violencia),
  id_caracterizacion  BIGINT NOT NULL REFERENCES caracterizaciones(id_caracterizacion),

  fecha_atencion      DATE NOT NULL,
  parentesco          TEXT,
  observaciones       TEXT,

  estado              BOOLEAN NOT NULL DEFAULT TRUE,
  creado_en           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  actualizado_en      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE TRIGGER tg_atenciones_updated
BEFORE UPDATE ON atenciones
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE INDEX IF NOT EXISTS ix_atenciones_fecha ON atenciones (fecha_atencion);
CREATE INDEX IF NOT EXISTS ix_atenciones_dimensiones ON atenciones (id_municipio, id_tipo_violencia, id_caracterizacion);
CREATE INDEX IF NOT EXISTS ix_personas_genero ON personas (id_genero);