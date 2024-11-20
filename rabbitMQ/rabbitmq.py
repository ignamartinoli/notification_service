import pika
import time
import os
import json

import pika.exceptions

"""
Función para conectar a RabbitMQ con reintentos.
"""
def connect_to_rabbitmq():
    rabbitmq_host = os.getenv("RABBITMQ_HOST", "localhost")
    connection = None
    for attempt in range(5): #Intentos de reconexión
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitmq_host))
            print("Conectado a RabbitMQ")
            break
        except pika.exceptions.AMQPConnectionError:
            print("Procesando...")
            print(f"Intento {attempt + 1} de conexión a RabbitMQ fallido. Reintentando en 5 segundos...")
            time.sleep(5)
    
    if connection is None:
        raise Exception("No se pudo conectar a RabbitMQ después de varios intentos")
    
    return connection

"""
Función para publicar un mensaje en la cola especificada
"""
def publish_message(channel, queue, message):
    channel.basic_publish(
        exchange='',
        routing_key=queue,
        body=json.dumps(message),
        properties=pika.BasicProperties(
            delivery_mode=2, #Mensaje persistente
        )
    )
    print(f"Mensaje enviado a la cola '{queue}: {message}")

