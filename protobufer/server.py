import sys
import os
from concurrent import futures
import grpc
from notification_pb2_grpc import NotificationServiceServicer, NotificationService, add_NotificationServiceServicer_to_server
import notification_pb2
from datetime import datetime
import uuid
from sqlalchemy.orm import sessionmaker ,Session
from sqlalchemy import create_engine, Column, String, DateTime
from enum import Enum
from sqlalchemy.ext.declarative import declarative_base

#project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
#sys.path.append(project_root)

#protobufer_path = os.path.join(project_root, 'protobufer')
#sys.path.append(protobufer_path)

# Configuración de la Base de Datos
DATABASE_URL = "sqlite:///./test.db"  # Se deja la URL de la base de datos de SQLite

# Crear la instancia del motor de la base de datos
engine = create_engine(DATABASE_URL)

# Crear la sesión de forma local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear la base de datos y el modelo
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
    tipo = Column(String)  # Tipo: email o sms
    fecha_envio = Column(DateTime)
    estado = Column(String, default=EstadoNotificacion.pendiente)  # Tipo: enviado o pendiente

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Crear la sesión
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class NotificationService(NotificationServiceServicer):
    def SendNotification(self, request, context):
        db: Session = next(get_db())
        
        # Crear la nueva notificación
        new_notification = Notificacion(
            id=str(uuid.uuid4()),  # Generar un ID único para la notificación
            usuario_id=request.usuarioId,
            mensaje=request.mensaje,
            tipo=request.tipo,
            fecha_envio=datetime.utcnow(),
            estado="enviado"  # Estado por defecto es "enviado"
        )

        # Guardar la notificación en la base de datos
        db.add(new_notification)
        db.commit()
        db.refresh(new_notification)

        # Responder con la notificación creada
        return notification_pb2.Notification(
            id=new_notification.id,
            usuarioId=new_notification.usuario_id,
            mensaje=new_notification.mensaje,
            tipo=new_notification.tipo,
            fechaEnvio=str(new_notification.fecha_envio),
            estado=new_notification.estado
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_NotificationServiceServicer_to_server(NotificationService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Servidor gRPC corriendo en el puerto 50051")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
