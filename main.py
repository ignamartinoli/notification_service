from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid
from models import Notification, SessionLocal

app = FastAPI()


class NotificationRequest(BaseModel):
    usuario_id: str
    mensaje: str
    tipo: str


@app.post("/notificaciones")
def send_notification(request: NotificationRequest):
    db = SessionLocal()
    notification = Notification(
        id=str(uuid.uuid4()),
        usuario_id=request.usuario_id,
        mensaje=request.mensaje,
        tipo=request.tipo,
        estado="pendiente",
    )
    db.add(notification)
    db.commit()
    db.refresh(notification)
    return notification


@app.get("/notificaciones/{id}")
def get_notification(id: str):
    db = SessionLocal()
    notification = db.query(Notification).filter(Notification.id == id).first()
    if notification is None:
        raise HTTPException(status_code=404, detail="Notificación no encontrada")
    return notification
