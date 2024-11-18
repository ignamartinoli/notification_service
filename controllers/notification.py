#Controlador Notificaciones

from uuid import uuid4
from models import Notificacion
from schemas import NotificationRequest, TipoNotificacion
from config.db import get_db
from fastapi import HTTPException

#Función para crear una nueva notificación
def create_notification(request: NotificationRequest):
    db = next(get_db())
    try:
        #Se valida que el tipo de notificación sea el esperado
        if request.tipo not in TipoNotificacion.__members__.values():
            raise HTTPException(status_code=400, detail="Tipo de notificación no válida. Debe ser 'email o 'sms'.")
        notification_id = str(uuid4())

        #Se crea una notificación
        new_notification = Notificacion(
            id = notification_id,
            usuario_id = request.usuario_id,
            mensaje = request.mensaje,
            tipo = request.tipo,
            #estado = "pendiente" Ya esta definido en el modelo el valor por defecto,
        )

        #Se agrega y se guarda la notificación en la BD
        db.add(new_notification)
        db.commit()
        db.refresh(new_notification)

        return new_notification
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al intentar crear la notificación: {str(e)}")
    
    finally:
        db.close()

#Función para devolver todas las notificaciones registradas
def get_all_notifications():
    db = next(get_db())
    try:
        #Se obtienen todas las notificaciones
        notifications = db.query(Notificacion).all()
        return notifications
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al intentar obtener las notificaciones: {str(e)}")
    finally:
        db.close()

#Función para devolver una notificación en base a su ID
def get_notification_by_id(id: str):
    db = next(get_db())
    try:
        notification = db.query(Notificacion).filter(Notificacion.id == id).first()
        if not notification:
            raise HTTPException(status_code=404, detail="Notificación no encontrada")
        return notification
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al intentar obtener una notificación: {str(e)}")
    finally:
        db.close()