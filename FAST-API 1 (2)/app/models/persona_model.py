from pydantic import BaseModel

class PersonaCreate(BaseModel):
    documento: str
    id_genero: int
    id_nacionalidad: int
    edad: int