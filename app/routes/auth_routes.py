from fastapi import APIRouter
from models.usuario_model import Usuario
from controllers.auth_controller import AuthController

router = APIRouter()
auth_controller = AuthController()

@router.post("/register")
async def register(usuario: Usuario):
    return auth_controller.register_user(usuario)