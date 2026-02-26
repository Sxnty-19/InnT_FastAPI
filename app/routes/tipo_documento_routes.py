from fastapi import APIRouter
from models.tipo_documento_model import TipoDocumento
from controllers.tipo_documento_controller import TipoDocumentoController

router = APIRouter()
tipo_documento_controller = TipoDocumentoController()

@router.post("/")
async def create_tipo_documento(tipo: TipoDocumento):
    return tipo_documento_controller.create_tipo_documento(tipo)

@router.get("/")
async def get_tipos_documento():
    return tipo_documento_controller.get_tipos_documento()

@router.get("/{id_tdocumento}")
async def get_tipo_documento_by_id(id_tdocumento: int):
    return tipo_documento_controller.get_tipo_documento_by_id(id_tdocumento)