#Consumidor del mensaje

import json
from datetime import datetime
from sqlalchemy.orm import Session
from rabbitMQ.rabbitmq import connect_to_rabbitmq
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
        
        if notification:
            #Se cambia el estado de la notificación a "enviado"
            notification.estado = "enviado"
            notification.fecha_envio = datetime.utcnow()
            notification.mensaje = "Pedido recibido y en Proceso"
            db.commit()
            print(f"Notificación para el usuario {message["usuarioId"]}")
        
        # Se confirma que el mensaje ha sido procesado correctamente
        ch.basic_ack(delivery_tag=method.delivery_tag)
    
    except Exception as e:
        print(f"Error procesando el mensaje : {e}")

#Se conecta a RabbitMQ y se configura el consumidor
connection = connect_to_rabbitmq()
channel = connection.channel()

#Se declara la cola 'pedidos.creados'
channel.queue_declare(queue="pedidos.creados")

#Se configura el consumidor para escuchar los mensajes en la cola 'pedidos.creados'
channel.basic_consume(queue="pedidos.creados", on_message_callback=callback)

# Se inicia el consumo de mensajes
print("Esperando mensajes en la cola 'pedidos.creados'.")
channel.start_consuming()