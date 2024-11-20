from fastapi import APIRouter
from controllers.notification import create_notification, get_all_notifications, get_notification_by_id
from schemas import NotificationRequest
from rabbitMQ.producer_pedidos import produce_pedidos_creados_messages

notification = APIRouter()

@notification.post("/notificaciones")
def post_notification(request: NotificationRequest):
    return create_notification(request)

@notification.get("/notificaciones")
def get_notifications():
    return get_all_notifications()

@notification.get("/notificaciones/{id}")
def get_notification(id: str):
    return get_notification_by_id(id=id)

@notification.post("/notificaciones/producir-pedidos")
def producir_pedidos():
    try:
        produce_pedidos_creados_messages()
        return {"message": "Mensajes enviados a la cola 'pedidos.creados'."}
    except Exception as e:
        return {"message": f"Error al enviar mensajes: {str(e)}"}