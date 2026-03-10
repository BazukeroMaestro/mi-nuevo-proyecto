from fastapi import APIRouter
from controllers.personas_controller import PersonasController
from models.persona_model import PersonaCreate

router = APIRouter(prefix="/personas", tags=["personas"])
controller = PersonasController()


@router.post("")
def crear_persona(data: PersonaCreate):
    return controller.crear_persona(data)


@router.get("")
def listar_personas():
    return controller.listar_personas()


@router.put("/{persona_id}")
def actualizar_persona(persona_id: int, data: PersonaCreate):
    return controller.actualizar_persona(persona_id, data)


@router.delete("/{persona_id}")
def eliminar_persona(persona_id: int):
    return controller.eliminar_persona(persona_id)