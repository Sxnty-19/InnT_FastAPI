from fastapi import APIRouter
from controllers.documento_controller import DocumentoController
from models.documento_model import Documento

router = APIRouter()
documento_controller = DocumentoController()

# Crear documento
@router.post("/")
def create_documento(documento: Documento):
    return documento_controller.create_documento(documento)

# Obtener todos los documentos
@router.get("/")
def get_documentos():
    return documento_controller.get_documentos()

# Obtener documento por ID
@router.get("/{id_documento}")
def get_documento_by_id(id_documento: int):
    return documento_controller.get_documento_by_id(id_documento)

# Obtener documentos de un usuario
@router.get("/usuario/{id_usuario}")
def get_documentos_por_usuario(id_usuario: int):
    return documento_controller.get_documentos_por_usuario(id_usuario)

# Buscar usuario por número de documento
@router.get("/buscar/{numero_documento}")
def buscar_usuario_por_documento(numero_documento: str):
    return documento_controller.buscar_usuario_por_documento(numero_documento)