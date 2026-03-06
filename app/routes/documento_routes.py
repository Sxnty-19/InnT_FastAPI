from fastapi import APIRouter, Depends
from utils.auth_utils import verificar_token
from models.documento_model import Documento
from controllers.documento_controller import DocumentoController

router = APIRouter()
documento_controller = DocumentoController()

@router.post("/c")
async def create_documento(documento: Documento):
    return documento_controller.create_documento(documento)

@router.get("/r")
async def get_documentos():
    return documento_controller.get_documentos()

@router.get("/r/{id_documento}")
async def get_documento_by_id(id_documento: int):
    return documento_controller.get_documento_by_id(id_documento)