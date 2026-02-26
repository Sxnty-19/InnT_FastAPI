from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.rol_routes import router as rol_router
from routes.usuario_routes import router as usuario_router
from routes.modulo_routes import router as modulo_router

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

#uvicorn main:app --reload
#fastapi dev main.py