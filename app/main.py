from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.rol_routes import router as rol_router
from routes.usuario_routes import router as usuario_router
from routes.modulo_routes import router as modulo_router
from routes.modulo_rol_routes import router as modulo_rol_router
from routes.tipo_documento_routes import router as tipo_documento_router
from routes.documento_routes import router as documento_router
from routes.tipo_habitacion_routes import router as tipo_habitacion_router
from routes.habitacion_routes import router as habitacion_router
from routes.reserva_routes import router as reserva_router

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
app.include_router(tipo_habitacion_router, prefix="/tipos-habitacion", tags=["Tipos de Habitación"])
app.include_router(habitacion_router, prefix="/habitaciones", tags=["Habitaciones"])
app.include_router(reserva_router, prefix="/reservas", tags=["Reservas"])

#uvicorn main:app --reload
#fastapi dev main.py