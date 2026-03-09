from fastapi import APIRouter
from controllers.habitacion_controller import HabitacionController
from models.habitacion_model import Habitacion

router = APIRouter()
habitacion_controller = HabitacionController()

# Crear habitación
@router.post("/")
def create_habitacion(habitacion: Habitacion):
    return habitacion_controller.create_habitacion(habitacion)

# Obtener todas las habitaciones
@router.get("/")
def get_habitaciones():
    return habitacion_controller.get_habitaciones()

# Obtener habitación por ID
@router.get("/{id_habitacion}")
def get_habitacion_by_id(id_habitacion: int):
    return habitacion_controller.get_habitacion_by_id(id_habitacion)

# Actualizar limpieza
@router.put("/limpieza/{id_habitacion}")
def actualizar_limpieza(id_habitacion: int):
    return habitacion_controller.actualizar_limpieza_por_id(id_habitacion)

# Obtener habitaciones disponibles
@router.get("/disponibles/")
def get_habitaciones_disponibles(date_start: str, date_end: str):
    return habitacion_controller.get_habitaciones_disponibles(date_start, date_end)