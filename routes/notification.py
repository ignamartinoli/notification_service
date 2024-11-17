from fastapi import APIRouter
from controllers.notification import create_notification
from schemas import NotificationRequest

notification = APIRouter()

@notification.post("/notificaciones")
def post_notification(request: NotificationRequest):
    return create_notification(request)