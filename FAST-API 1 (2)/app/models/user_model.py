from pydantic import BaseModel

# 🔹 Modelo para crear y actualizar
class UserCreate(BaseModel):
    nombre: str
    usuario: str
    cedula: str
    edad: int
    email: str
    contrasena: str
    rol: str