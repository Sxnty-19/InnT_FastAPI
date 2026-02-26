from fastapi import APIRouter
from models.habitacion_model import Habitacion
from controllers.habitacion_controller import HabitacionController

router = APIRouter()
habitacion_controller = HabitacionController()

@router.post("/")
async def create_habitacion(habitacion: Habitacion):
    return habitacion_controller.create_habitacion(habitacion)

@router.get("/")
async def get_habitaciones():
    return habitacion_controller.get_habitaciones()

@router.get("/{id_habitacion}")
async def get_habitacion_by_id(id_habitacion: int):
    return habitacion_controller.get_habitacion_by_id(id_habitacion)