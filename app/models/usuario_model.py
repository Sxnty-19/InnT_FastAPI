from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class Usuario(BaseModel):
    id_usuario: Optional[int] = None
    id_rol: Optional[int] = 3
    primer_nombre: str
    segundo_nombre: Optional[str] = None
    primer_apellido: str
    segundo_apellido: Optional[str] = None
    telefono: Optional[str] = None
    correo: Optional[EmailStr] = None 
    username: str
    password: str
    estado: Optional[bool] = True
    date_created: Optional[datetime] = None
    date_updated: Optional[datetime] = None