from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.rol_routes import router as rol_router
from routes.usuario_routes import router as usuario_router
from routes.modulo_routes import router as modulo_router
from routes.modulo_rol_routes import router as modulo_rol_router
from routes.tipo_documento_routes import router as tipo_documento_router
from routes.documento_routes import router as documento_router
from controllers.tipo_habitacion_controller import TipoHabitacionController

app = FastAPI(
    title="InnT API",
    description="Backend desarrollado con FastAPI.",
    version="2.3.5"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(rol_router, prefix="/roles", tags=["Roles"])
app.include_router(usuario_router, prefix="/usuarios", tags=["Usuarios"])
app.include_router(modulo_router, prefix="/modulos", tags=["Módulos"])
app.include_router(modulo_rol_router, prefix="/modulos-roles", tags=["Módulos-Roles"])
app.include_router(tipo_documento_router, prefix="/tipos-documento", tags=["Tipos de Documento"])
app.include_router(documento_router, prefix="/documentos", tags=["Documentos"])
app.include_router(TipoHabitacionController(), prefix="/tipos-habitacion", tags=["Tipos de Habitación"])

#uvicorn main:app --reload
#fastapi dev main.py