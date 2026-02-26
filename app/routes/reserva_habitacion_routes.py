from fastapi import APIRouter
from models.reserva_habitacion_model import ReservaHabitacion
from controllers.reserva_habitacion_controller import ReservaHabitacionController

router = APIRouter()
reserva_habitacion_controller = ReservaHabitacionController()

@router.post("/")
async def create_reserva_habitacion(reserva_habitacion: ReservaHabitacion):
    return reserva_habitacion_controller.create_reserva_habitacion(reserva_habitacion)

@router.get("/")
async def get_reservas_habitaciones():
    return reserva_habitacion_controller.get_reservas_habitaciones()

@router.get("/{id_rxh}")
async def get_reserva_habitacion_by_id(id_rxh: int):
    return reserva_habitacion_controller.get_reserva_habitacion_by_id(id_rxh)