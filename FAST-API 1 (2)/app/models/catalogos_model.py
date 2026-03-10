from typing import Optional
from pydantic import BaseModel

class Municipio(BaseModel):
    id: Optional[int] = None
    nombre: str

class Eps(BaseModel):
    id: Optional[int] = None
    nombre: str

class Escolaridad(BaseModel):
    id: Optional[int] = None
    nivel: str

class Ocupacion(BaseModel):
    id: Optional[int] = None
    ocupacion: str

class CatalogoCreate(BaseModel):
    nombre: str