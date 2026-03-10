from fastapi import APIRouter
from controllers.auth_controller import AuthController
from models.auth_model import LoginRequest

router = APIRouter(prefix="/auth", tags=["auth"])
controller = AuthController()

@router.post("/login")
def login(data: LoginRequest):
    return controller.login(data.email, data.password)