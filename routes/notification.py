from fastapi import APIRouter
from controllers.notification import create_notification, get_all_notifications, get_notification_by_id
from schemas import NotificationRequest

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