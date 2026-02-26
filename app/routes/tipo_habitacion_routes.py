from fastapi import APIRouter
from models.tipo_habitacion_model import TipoHabitacion
from controllers.tipo_habitacion_controller import TipoHabitacionController

router = APIRouter()
tipo_habitacion_controller = TipoHabitacionController()

@router.post("/")
async def create_tipo_habitacion(tipo: TipoHabitacion):
    return tipo_habitacion_controller.create_tipo_habitacion(tipo)

@router.get("/")
async def get_tipos_habitacion():
    return tipo_habitacion_controller.get_tipos_habitacion()

@router.get("/{id_thabitacion}")
async def get_tipo_habitacion_by_id(id_thabitacion: int):
    return tipo_habitacion_controller.get_tipo_habitacion_by_id(id_thabitacion)