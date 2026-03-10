from fastapi import APIRouter, Depends, HTTPException
from controllers.roles_controller import RolesController
from models.role_model import RoleUpdate
from security import require_role

router = APIRouter(prefix="/roles", tags=["roles"])

ctrl = RolesController()

# SOLO ADMIN
@router.get("/lista")
def roles_list(current = Depends(require_role("ADMIN"))):
    return ctrl.list_roles()

# SOLO ADMIN
@router.get("/usuarios")
def usuarios_list(current = Depends(require_role("ADMIN"))):
    return ctrl.list_users()

# SOLO ADMIN
@router.patch("/cambiar/{user_id}")
def cambiar_rol(user_id: int, data: RoleUpdate, current = Depends(require_role("ADMIN"))):
    return ctrl.change_role(user_id, data.rol)

# SOLO ADMIN
@router.delete("/usuarios/{user_id}")
def eliminar_usuario(
    user_id: int,
    current = Depends(require_role("ADMIN"))
):
    try:
        return ctrl.delete_user(user_id)
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Error eliminando usuario"
        )


# SOLO ADMIN
@router.patch("/usuarios/{user_id}/estado")
def cambiar_estado_usuario(
    user_id: int,
    current = Depends(require_role("ADMIN"))
):
    try:
        return ctrl.toggle_user_status(user_id)
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Error cambiando estado del usuario"
        )
