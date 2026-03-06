from fastapi import APIRouter, Depends
from utils.auth_utils import verificar_token
from models.rol_model import Rol
from controllers.rol_controller import RolController

router = APIRouter()
rol_controller = RolController()

@router.post("/c")
async def create_rol(rol: Rol):
    return rol_controller.create_rol(rol)

@router.get("/r")
async def get_roles():
    return rol_controller.get_roles()

@router.get("/r/{id_rol}")
async def get_rol_by_id(id_rol: int):
    return rol_controller.get_rol_by_id(id_rol)