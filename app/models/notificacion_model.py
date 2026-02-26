from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Notificacion(BaseModel):
    id_notificacion: Optional[int] = None
    id_usuario: int
    id_habitacion: int
    descripcion: str
    estado: Optional[bool] = True
    date_created: Optional[datetime] = None
    date_updated: Optional[datetime] = None