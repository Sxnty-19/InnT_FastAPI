from fastapi import APIRouter, Depends
from utils.auth_utils import verificar_token
from models.habitacion_model import Habitacion
from controllers.habitacion_controller import HabitacionController

router = APIRouter()
habitacion_controller = HabitacionController()

@router.post("/c")
async def create_habitacion(habitacion: Habitacion):
    return habitacion_controller.create_habitacion(habitacion)

@router.get("/r")
async def get_habitaciones():
    return habitacion_controller.get_habitaciones()

@router.get("/r/{id_habitacion}")
async def get_habitacion_by_id(id_habitacion: int):
    return habitacion_controller.get_habitacion_by_id(id_habitacion)