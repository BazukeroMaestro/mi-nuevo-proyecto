from pydantic import BaseModel

class TipoViolenciaCreate(BaseModel):
    codigo: str
    descripcion: str | None = None