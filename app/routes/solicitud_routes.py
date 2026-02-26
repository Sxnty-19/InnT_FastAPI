from fastapi import APIRouter
from models.solicitud_model import Solicitud
from controllers.solicitud_controller import SolicitudController

router = APIRouter()
solicitud_controller = SolicitudController()

@router.post("/")
async def create_solicitud(solicitud: Solicitud):
    return solicitud_controller.create_solicitud(solicitud)

@router.get("/")
async def get_solicitudes():
    return solicitud_controller.get_solicitudes()

@router.get("/{id_solicitud}")
async def get_solicitud_by_id(id_solicitud: int):
    return solicitud_controller.get_solicitud_by_id(id_solicitud)