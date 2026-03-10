from pydantic import BaseModel
from datetime import date

class AtencionCreate(BaseModel):
    id_persona: int
    id_municipio: int
    id_eps: int
    id_escolaridad: int
    id_ocupacion: int
    id_tipo_violencia: int
    id_caracterizacion: int
    fecha_atencion: date
    parentesco: str
    observaciones: str