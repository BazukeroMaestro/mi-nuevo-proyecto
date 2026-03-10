from fastapi import APIRouter
from controllers.atenciones_controller import AtencionesController
from models.atencion_model import AtencionCreate

router = APIRouter(prefix="/atenciones", tags=["atenciones"])
controller = AtencionesController()


@router.post("")
def crear_atencion(data: AtencionCreate):
    return controller.crear_atencion(data)


@router.get("")
def listar_atenciones():
    return controller.listar_atenciones()


@router.put("/{atencion_id}")
def actualizar_atencion(atencion_id: int, data: AtencionCreate):
    return controller.actualizar_atencion(atencion_id, data)


@router.delete("/{atencion_id}")
def eliminar_atencion(atencion_id: int):
    return controller.eliminar_atencion(atencion_id)