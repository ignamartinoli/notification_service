from pydantic import BaseModel
from enum import Enum

class TipoNotificacion(str, Enum):
    email = "email"
    sms = "sms"

class NotificationRequest(BaseModel):
    usuario_id: str
    mensaje: str
    tipo: TipoNotificacion

    class Config:
        orm_mode = True