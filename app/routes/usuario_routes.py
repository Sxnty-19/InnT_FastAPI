from fastapi import APIRouter
from models.usuario_model import Usuario
from controllers.usuario_controller import UsuarioController

router = APIRouter()
usuario_controller = UsuarioController()

@router.post("/")
async def create_usuario(usuario: Usuario):
    return usuario_controller.create_usuario(usuario)

@router.get("/")
async def get_usuarios():
    return usuario_controller.get_usuarios()

@router.get("/{id_usuario}")
async def get_usuario_by_id(id_usuario: int):
    return usuario_controller.get_usuario_by_id(id_usuario)