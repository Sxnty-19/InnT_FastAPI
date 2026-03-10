from fastapi import APIRouter,Depends
from controllers.modulo_rol_controller import ModuloRolController
from models.modulo_rol_model import ModuloRol
from utils.auth_utils import verificar_token

router = APIRouter()
modulo_rol_controller = ModuloRolController()

# Crear relación módulo-rol
@router.post("/")
def create_modulo_rol(modulo_rol: ModuloRol):
    return modulo_rol_controller.create_modulo_rol(modulo_rol)

# Obtener todas las relaciones
@router.get("/")
def get_modulos_roles():
    return modulo_rol_controller.get_modulos_roles()

# Obtener relación por id
@router.get("/{id_mxr}")
def get_modulo_rol_by_id(id_mxr: int):
    return modulo_rol_controller.get_modulo_rol_by_id(id_mxr)

# Obtener módulos según rol
@router.get("/rol/")
def get_modulos_by_rol(payload: dict = Depends(verify_token)):
    return modulo_rol_controller.get_modulos_by_rol(payload)