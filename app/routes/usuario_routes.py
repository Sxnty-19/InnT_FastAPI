from fastapi import APIRouter, Depends
from utils.auth_utils import verificar_token
from models.usuario_model import Usuario
from controllers.usuario_controller import UsuarioController

router = APIRouter()
usuario_controller = UsuarioController()

@router.post("/c")
async def create_usuario(usuario: Usuario):
    return usuario_controller.create_usuario(usuario)

@router.get("/r")
async def get_usuarios():
    return usuario_controller.get_usuarios()

@router.get("/r/{id_usuario}")
async def get_usuario_by_id(id_usuario: int):
    return usuario_controller.get_usuario_by_id(id_usuario)

@router.get("/r-token")
async def get_usuario(payload: dict = Depends(verificar_token)):
    return usuario_controller.get_usuario(payload)

@router.patch("/u")
def update_usuario(usuario: Usuario, payload: dict = Depends(verificar_token)):
    data = usuario.dict(exclude_unset=True)
    return usuario_controller.update_usuario(data, payload)