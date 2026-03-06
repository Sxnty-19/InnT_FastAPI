from fastapi import APIRouter, Depends
from utils.auth_utils import verificar_token
from models.usuario_habitacion_model import UsuarioHabitacion
from controllers.usuario_habitacion_controller import UsuarioHabitacionController

router = APIRouter()
usuario_habitacion_controller = UsuarioHabitacionController()

@router.post("/c")
async def create_usuario_habitacion(usuario_habitacion: UsuarioHabitacion):
    return usuario_habitacion_controller.create_usuario_habitacion(usuario_habitacion)

@router.get("/r")
async def get_usuarios_habitaciones():
    return usuario_habitacion_controller.get_usuarios_habitaciones()

@router.get("/r/{id_uxh}")
async def get_usuario_habitacion_by_id(id_uxh: int):
    return usuario_habitacion_controller.get_usuario_habitacion_by_id(id_uxh)