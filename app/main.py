from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from utils.auth_utils import verificar_token

from routes.auth_routes import router as auth_router

from routes.rol_routes import router as rol_router
from routes.usuario_routes import router as usuario_router
from routes.modulo_routes import router as modulo_router
from routes.modulo_rol_routes import router as modulo_rol_router
from routes.tipo_documento_routes import router as tipo_documento_router
from routes.documento_routes import router as documento_router
from routes.tipo_habitacion_routes import router as tipo_habitacion_router
from routes.habitacion_routes import router as habitacion_router
from routes.reserva_routes import router as reserva_router
from routes.reserva_habitacion_routes import router as reserva_habitacion_router
from routes.usuario_habitacion_routes import router as usuario_habitacion_router
from routes.solicitud_routes import router as solicitud_router

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

@app.api_route("/", methods=["GET"], tags=["Sistema"])
async def root():
    return {"message": "API en funcionamiento..."}

app.include_router(auth_router, prefix="/auth", tags=["Autenticación"])

app.include_router(rol_router, prefix="/roles", tags=["Roles"], dependencies=[Depends(verificar_token)])
app.include_router(usuario_router, prefix="/usuarios", tags=["Usuarios"], dependencies=[Depends(verificar_token)])
app.include_router(modulo_router, prefix="/modulos", tags=["Módulos"], dependencies=[Depends(verificar_token)])
app.include_router(modulo_rol_router, prefix="/modulos-roles", tags=["Módulos-Roles"], dependencies=[Depends(verificar_token)])
app.include_router(tipo_documento_router, prefix="/tipos-documento", tags=["Tipos de Documento"], dependencies=[Depends(verificar_token)])
app.include_router(documento_router, prefix="/documentos", tags=["Documentos"],dependencies=[Depends(verificar_token)])
app.include_router(tipo_habitacion_router, prefix="/tipos-habitacion", tags=["Tipos de Habitación"],dependencies=[Depends(verificar_token)])
app.include_router(habitacion_router, prefix="/habitaciones", tags=["Habitaciones"], dependencies=[Depends(verificar_token)])
app.include_router(reserva_router, prefix="/reservas", tags=["Reservas"], dependencies=[Depends(verificar_token)])
app.include_router(reserva_habitacion_router, prefix="/reservas-habitaciones", tags=["Reservas-Habitaciones"], dependencies=[Depends(verificar_token)])
app.include_router(usuario_habitacion_router, prefix="/usuarios-habitaciones", tags=["Usuarios-Habitaciones"], dependencies=[Depends(verificar_token)])
app.include_router(solicitud_router, prefix="/solicitudes", tags=["Solicitudes"], dependencies=[Depends(verificar_token)])

#uvicorn main:app --reload
#fastapi dev main.py

#http://127.0.0.1:8000 (Local)
#https://innt-fastapi.onrender.com (Render)