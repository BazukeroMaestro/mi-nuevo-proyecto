from fastapi import APIRouter, HTTPException, status, Depends
from controllers.user_controller import UserController
from models.user_model import UserCreate
from security import get_current_user

router = APIRouter(tags=["users"])
nuevo_usuario = UserController()

@router.post("/create_user", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    return nuevo_usuario.create_user(user)

@router.get("/get_user/{user_id}")
def get_user(user_id: int, user=Depends(get_current_user)):
    return nuevo_usuario.get_user(user_id)

@router.get("/get_users/")
def get_users(user=Depends(get_current_user)):
    return nuevo_usuario.get_users()

@router.put("/update_user/{user_id}")
def update_user(user_id: int, user: UserCreate, current=Depends(get_current_user)):
    return nuevo_usuario.update_user(user_id, user)

@router.delete("/delete_user/{user_id}")
def delete_user(user_id: int, current=Depends(get_current_user)):
    return nuevo_usuario.delete_user(user_id)