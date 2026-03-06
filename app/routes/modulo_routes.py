from fastapi import APIRouter, Depends
from utils.auth_utils import verificar_token
from models.modulo_model import Modulo
from controllers.modulo_controller import ModuloController

router = APIRouter()
modulo_controller = ModuloController()

@router.post("/c")
async def create_modulo(modulo: Modulo):
    return modulo_controller.create_modulo(modulo)

@router.get("/r")
async def get_modulos():
    return modulo_controller.get_modulos()

@router.get("/r/{id_modulo}")
async def get_modulo_by_id(id_modulo: int):
    return modulo_controller.get_modulo_by_id(id_modulo)