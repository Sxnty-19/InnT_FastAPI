from fastapi import APIRouter
from models.reserva_model import Reserva
from controllers.reserva_controller import ReservaController

router = APIRouter()
reserva_controller = ReservaController()

@router.post("/")
async def create_reserva(reserva: Reserva):
    return reserva_controller.create_reserva(reserva)

@router.get("/")
async def get_reservas():
    return reserva_controller.get_reservas()

@router.get("/{id_reserva}")
async def get_reserva_by_id(id_reserva: int):
    return reserva_controller.get_reserva_by_id(id_reserva)