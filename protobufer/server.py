import sys
import os
from concurrent import futures
import grpc
#from ..models.notification import EstadoNotificacion, Notificacion
import notification_pb2
import notification_pb2_grpc
#from protobufer import notification_pb2, notification_pb2_grpc

from datetime import datetime
import uuid
from sqlalchemy.orm import Session
#from models.notification import *
from models.notification import EstadoNotificacion, Notificacion
from config.db import engine
from sqlalchemy.orm import sessionmaker

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

protobufer_path = os.path.join(project_root, 'protobufer')
sys.path.append(protobufer_path)

# Crear la conexión a la base de datos
DATABASE_URL = "sqlite:///./test.db" 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear la sesión
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class NotificationService(notification_pb2_grpc.NotificationServiceServicer):
    def SendNotification(self, request, context):
        db: Session = next(get_db())
        
        # Crear la nueva notificación
        new_notification = Notificacion(
            id=str(uuid.uuid4()),  # Generar un ID único para la notificación
            usuario_id=request.usuarioId,
            mensaje=request.mensaje,
            tipo=request.tipo,
            fecha_envio=datetime.utcnow(),
            estado=EstadoNotificacion.enviado  # Estado por defecto es "enviado"
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
    notification_pb2_grpc.add_NotificationServiceServicer_to_server(NotificationService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Servidor gRPC corriendo en el puerto 50051")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
