from fastapi import APIRouter, Depends
from utils.auth_utils import verificar_token
from models.modulo_rol_model import ModuloRol
from controllers.modulo_rol_controller import ModuloRolController

router = APIRouter()
modulo_rol_controller = ModuloRolController()

@router.post("/c")
async def create_modulo_rol(modulo_rol: ModuloRol):
    return modulo_rol_controller.create_modulo_rol(modulo_rol)

@router.get("/r")
async def get_modulos_roles():
    return modulo_rol_controller.get_modulos_roles()

@router.get("/r/{id_mxr}")
async def get_modulo_rol_by_id(id_mxr: int):
    return modulo_rol_controller.get_modulo_rol_by_id(id_mxr)

@router.get("/r-modulos-rol")
def get_modulos_by_rol(payload: dict = Depends(verificar_token)):
    return modulo_rol_controller.get_modulos_by_rol(payload)