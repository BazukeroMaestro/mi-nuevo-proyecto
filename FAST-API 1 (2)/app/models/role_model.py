from pydantic import BaseModel

class RoleUpdate(BaseModel):
    rol: str  # ADMIN, ANALISTA o CONSULTA