from fastapi import APIRouter
from models.modulo_model import Modulo
from controllers.modulo_controller import ModuloController

router = APIRouter()
modulo_controller = ModuloController()

@router.post("/")
async def create_modulo(modulo: Modulo):
    return modulo_controller.create_modulo(modulo)

@router.get("/")
async def get_modulos():
    return modulo_controller.get_modulos()

@router.get("/{id_modulo}")
async def get_modulo_by_id(id_modulo: int):
    return modulo_controller.get_modulo_by_id(id_modulo)