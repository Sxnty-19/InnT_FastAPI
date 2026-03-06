from fastapi import APIRouter, Depends
from utils.auth_utils import verificar_token
from models.reserva_habitacion_model import ReservaHabitacion
from controllers.reserva_habitacion_controller import ReservaHabitacionController

router = APIRouter()
reserva_habitacion_controller = ReservaHabitacionController()

@router.post("/c")
async def create_reserva_habitacion(reserva_habitacion: ReservaHabitacion):
    return reserva_habitacion_controller.create_reserva_habitacion(reserva_habitacion)

@router.get("/r")
async def get_reservas_habitaciones():
    return reserva_habitacion_controller.get_reservas_habitaciones()

@router.get("/r/{id_rxh}")
async def get_reserva_habitacion_by_id(id_rxh: int):
    return reserva_habitacion_controller.get_reserva_habitacion_by_id(id_rxh)