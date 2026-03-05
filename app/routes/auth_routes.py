from fastapi import APIRouter, Form
from models.usuario_model import Usuario
from controllers.auth_controller import AuthController

router = APIRouter()
auth_controller = AuthController()

@router.post("/register")
async def register_user(usuario: Usuario):
    return auth_controller.register_user(usuario)

@router.post("/login")
async def login_user(username: str = Form(...), password: str = Form(...)):
    return auth_controller.login_user(username, password)