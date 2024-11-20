import json 
from .rabbitmq import connect_to_rabbitmq, publish_message

def produce_pedidos_creados_messages():
    connection = connect_to_rabbitmq()
    channel = connection.channel()

    #Se declara la cola 'pedidos.creados'

    channel.queue_declare(queue='pedidos.creados')

    #Se simula una lista de mensajes a enviar
    messages = [
        {
           "id": "880e8400-e29b-41d4-a716-446655440001",
            "usuarioId": "550e8400-e29b-41d4-a716-446655440001",
            "fechaCreacion": "2023-10-02T16:00:00Z",
        },
        {
            "id": "880e8400-e29b-41d4-a716-446655440000",
            "usuarioId": "550e8400-e29b-41d4-a716-446655440000",
            "fechaCreacion": "2023-10-01T16:00:00Z",
        },
    ]

    #Se envia los mensajes
    for message in messages:
        publish_message(channel, 'pedidos.creados', message)
    
    connection.close()

if __name__ == "__main__":
    produce_pedidos_creados_messages()