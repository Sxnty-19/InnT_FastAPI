from fastapi import APIRouter
from controllers.rol_controller import RolController
from models.rol_model import Rol

router = APIRouter()
rol_controller = RolController()

@router.post("/")
async def create_rol(rol: Rol):
    return rol_controller.create_rol(rol)

@router.get("/")
async def get_roles():
    return rol_controller.get_roles()

@router.get("/{id_rol}")
async def get_rol_by_id(id_rol: int):
    return rol_controller.get_rol_by_id(id_rol)