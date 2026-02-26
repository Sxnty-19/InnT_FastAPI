from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

#from routes.auth_routes import router as auth_router
from routes.usuario_routes import router as usuario_router

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

#app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(usuario_router, prefix="/usuarios", tags=["Usuarios"])