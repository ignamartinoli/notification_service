import pika
import json
from datetime import datetime
from sqlalchemy.orm import Session
from .rabbitmq import connect_to_rabbitmq
from config.db import get_db
from models import Notificacion

#Función que se ejecuta cuando se recibe un mensaje
def callback(ch, method, properties, body):
    try:
        #Se decodifica el mensaje recibido
        message = json.loads(body)
        print(f"Mensaje recibido: {message}")

        db: Session = next(get_db())

        #Se busca la notificación correspondiente al usuario
        notification = db.query(Notificacion).filter(Notificacion.usuario_id == message["usuarioId"]).first()
        print("Valor de noti: ", notification)
        if notification:
            #Se cambia el estado de la notificación a "enviado"
            notification.estado = "enviado"
            notification.fecha_envio = datetime.utcnow()
            notification.mensaje = "Pedido recibido y en Proceso"
            print(f"Notificación para el usuario {message['usuarioId']}")
            db.add(notification)
        else:
            #Si no existe una notificación con ese usuarioId, se crea una nueva notificación
            new_notificaction = Notificacion(
                id=message["id"],
                usuario_id=message["usuarioId"],
                mensaje="Pedido recibido y en proceso",
                tipo="email",
                fecha_envio=datetime.utcnow(),
                estado="enviado"
            )
            db.add(new_notificaction)
            print(f"Nueva notificación creada para el usuario {message['usuarioId']}")
        
        db.commit()
        
        # Se confirma que el mensaje ha sido procesado correctamente
        ch.basic_ack(delivery_tag=method.delivery_tag)
    
    except Exception as e:
        print(f"Error procesando el mensaje : {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

# Conexión a RabbitMQ y configuración del canal
"""
def connect_to_rabbitmq():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
        print("Conexión exitosa a RabbitMQ.")
        return connection
    except Exception as e:
        print(f"Error al conectar con RabbitMQ: {e}")
        raise
"""

# Se conecta a RabbitMQ y se configura el consumidor
connection = connect_to_rabbitmq()
channel = connection.channel()

# Se declara la cola 'pedidos.creados'
channel.queue_declare(queue="pedidos.creados")

# Se configura el consumidor para escuchar los mensajes en la cola 'pedidos.creados'
channel.basic_consume(queue="pedidos.creados", on_message_callback=callback)

# Se inicia el consumo de mensajes
print("Esperando mensajes en la cola 'pedidos.creados'.")
channel.start_consuming()
