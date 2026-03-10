from fastapi import APIRouter
from controllers.catalogos_controller import CatalogosController
from models.catalogos_model import CatalogoCreate
from models.tipo_violencia_model import TipoViolenciaCreate
from models.caracterizacion_model import CaracterizacionCreate

router = APIRouter(prefix="/catalogos", tags=["catalogos"])
controller = CatalogosController()

# ================= MUNICIPIOS =================

@router.post("/municipios")
def create_municipio(data: CatalogoCreate):
    return controller.crear_municipio(data)

@router.get("/municipios")
def list_municipios():
    return controller.listar_municipios()

@router.put("/municipios/{item_id}")
def update_municipio(item_id: int, data: CatalogoCreate):
    return controller.actualizar_municipio(item_id, data)

@router.delete("/municipios/{item_id}")
def delete_municipio(item_id: int):
    return controller.eliminar_municipio(item_id)


# ================= EPS =================

@router.post("/eps")
def create_eps(data: CatalogoCreate):
    return controller.crear_eps(data)

@router.get("/eps")
def list_eps():
    return controller.listar_eps()

@router.put("/eps/{item_id}")
def update_eps(item_id: int, data: CatalogoCreate):
    return controller.actualizar_eps(item_id, data)

@router.delete("/eps/{item_id}")
def delete_eps(item_id: int):
    return controller.eliminar_eps(item_id)


# ================= ESCOLARIDADES =================

@router.post("/escolaridades")
def create_escolaridad(data: CatalogoCreate):
    return controller.crear_escolaridad(data)

@router.get("/escolaridades")
def list_escolaridades():
    return controller.listar_escolaridades()

@router.put("/escolaridades/{item_id}")
def update_escolaridad(item_id: int, data: CatalogoCreate):
    return controller.actualizar_escolaridad(item_id, data)

@router.delete("/escolaridades/{item_id}")
def delete_escolaridad(item_id: int):
    return controller.eliminar_escolaridad(item_id)


# ================= OCUPACIONES =================

@router.post("/ocupaciones")
def create_ocupacion(data: CatalogoCreate):
    return controller.crear_ocupacion(data)

@router.get("/ocupaciones")
def list_ocupaciones():
    return controller.listar_ocupaciones()

@router.put("/ocupaciones/{item_id}")
def update_ocupacion(item_id: int, data: CatalogoCreate):
    return controller.actualizar_ocupacion(item_id, data)

@router.delete("/ocupaciones/{item_id}")
def delete_ocupacion(item_id: int):
    return controller.eliminar_ocupacion(item_id)

# ================= GENEROS =================

@router.post("/generos")
def create_genero(data: CatalogoCreate):
    return controller.crear_genero(data)

@router.get("/generos")
def list_generos():
    return controller.listar_generos()

@router.put("/generos/{item_id}")
def update_genero(item_id: int, data: CatalogoCreate):
    return controller.actualizar_genero(item_id, data)

@router.delete("/generos/{item_id}")
def delete_genero(item_id: int):
    return controller.eliminar_genero(item_id)


# ================= NACIONALIDADES =================

@router.post("/nacionalidades")
def create_nacionalidad(data: CatalogoCreate):
    return controller.crear_nacionalidad(data)

@router.get("/nacionalidades")
def list_nacionalidades():
    return controller.listar_nacionalidades()

@router.put("/nacionalidades/{item_id}")
def update_nacionalidad(item_id: int, data: CatalogoCreate):
    return controller.actualizar_nacionalidad(item_id, data)

@router.delete("/nacionalidades/{item_id}")
def delete_nacionalidad(item_id: int):
    return controller.eliminar_nacionalidad(item_id)

# TIPOS VIOLENCIA

@router.post("/tipos-violencia")
def create_tipo_violencia(data: TipoViolenciaCreate):
    return controller.crear_tipo_violencia(data)

@router.get("/tipos-violencia")
def list_tipos_violencia():
    return controller.listar_tipos_violencia()

@router.put("/tipos-violencia/{item_id}")
def update_tipo_violencia(item_id: int, data: TipoViolenciaCreate):
    return controller.actualizar_tipo_violencia(item_id, data)

@router.delete("/tipos-violencia/{item_id}")
def delete_tipo_violencia(item_id: int):
    return controller.eliminar_tipo_violencia(item_id)


# CARACTERIZACIONES

@router.post("/caracterizaciones")
def create_caracterizacion(data: CaracterizacionCreate):
    return controller.crear_caracterizacion(data)

@router.get("/caracterizaciones")
def list_caracterizaciones():
    return controller.listar_caracterizaciones()

@router.put("/caracterizaciones/{item_id}")
def update_caracterizacion(item_id: int, data: CaracterizacionCreate):
    return controller.actualizar_caracterizacion(item_id, data)

@router.delete("/caracterizaciones/{item_id}")
def delete_caracterizacion(item_id: int):
    return controller.eliminar_caracterizacion(item_id)