import pika
import time
import os
import json
from models import Notification, SessionLocal


def connect_to_rabbitmq():
    rabbitmq_host = os.getenv("RABBITMQ_HOST", "localhost")
    connection = None
    for attempt in range(5):  # Intentos de reconexión
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(rabbitmq_host)
            )
            print("Conectado a RabbitMQ")
            break
        except pika.exceptions.AMQPConnectionError:
            print(
                f"Intento {
                    attempt + 1} de conexión a RabbitMQ fallido. Reintentando en 5 segundos..."
            )
            time.sleep(5)
    if connection is None:
        raise Exception(
            "No se pudo conectar a RabbitMQ después de varios intentos.")
    return connection


connection = connect_to_rabbitmq()
channel = connection.channel()
channel.queue_declare(queue="pedidos.creados")


def callback(ch, method, properties, body):
    message = json.loads(body)
    db = SessionLocal()
    notification = (
        db.query(Notification)
        .filter(Notification.usuario_id == message["usuarioId"])
        .first()
    )
    if notification:
        notification.estado = "enviado"
        db.commit()
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(queue="pedidos.creados", on_message_callback=callback)
print("Esperando mensajes en la cola 'pedidos.creados'")
channel.start_consuming()
