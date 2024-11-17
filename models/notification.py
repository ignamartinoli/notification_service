from enum import Enum
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from config.db import engine

Base = declarative_base()

class TipoNotificacion(str, Enum):
    email = "email"
    sms = "sms"

class EstadoNotificacion(str, Enum):
    pendiente = "pendiente"
    enviado = "enviado"

class Notificacion(Base):
    __tablename__ = "notificaciones"
    id = Column(String, primary_key=True, index=True)
    usuario_id = Column(String, index=True)
    mensaje = Column(String(1000))
    tipo = Column(String) #Tipo: email o sms
    fecha_envio = Column(DateTime)
    estado = Column(String, default=EstadoNotificacion.pendiente) #Tipo: enviado o pendiente


Base.metadata.create_all(bind=engine)