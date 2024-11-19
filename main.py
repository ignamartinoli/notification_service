from fastapi import FastAPI
from routes.notification import notification

app = FastAPI()

@app.get("/")
def root():
    return "Bienvenido a la API del Servicio de Notificaciones"

app.include_router(notification)
