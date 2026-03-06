from fastapi import APIRouter, Depends
from utils.auth_utils import verificar_token
from models.reserva_model import Reserva
from controllers.reserva_controller import ReservaController

router = APIRouter()
reserva_controller = ReservaController()

@router.post("/c")
async def create_reserva(reserva: Reserva):
    return reserva_controller.create_reserva(reserva)

@router.get("/r")
async def get_reservas():
    return reserva_controller.get_reservas()

@router.get("/r/{id_reserva}")
async def get_reserva_by_id(id_reserva: int):
    return reserva_controller.get_reserva_by_id(id_reserva)