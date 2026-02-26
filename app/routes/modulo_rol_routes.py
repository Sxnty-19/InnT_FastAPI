from fastapi import APIRouter
from models.modulo_rol_model import ModuloRol
from controllers.modulo_rol_controller import ModuloRolController

router = APIRouter()
modulo_rol_controller = ModuloRolController()

@router.post("/")
async def create_modulo_rol(modulo_rol: ModuloRol):
    return modulo_rol_controller.create_modulo_rol(modulo_rol)

@router.get("/")
async def get_modulos_roles():
    return modulo_rol_controller.get_modulos_roles()

@router.get("/{id_mxr}")
async def get_modulo_rol_by_id(id_mxr: int):
    return modulo_rol_controller.get_modulo_rol_by_id(id_mxr)