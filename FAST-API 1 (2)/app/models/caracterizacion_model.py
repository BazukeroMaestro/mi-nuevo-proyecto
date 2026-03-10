from pydantic import BaseModel

class CaracterizacionCreate(BaseModel):
    caracterizacion_normalizada: str
    es_psicologica: bool = False
    es_fisica: bool = False
    es_sexual: bool = False
    es_economica: bool = False
    es_patrimonial: bool = False
    es_ciberacoso: bool = False