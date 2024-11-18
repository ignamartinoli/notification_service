#Productor del mensaje

from .rabbitmq import connect_to_rabbitmq, publish_message

def send_notification_message(message):
    try:
        #Se establece la conexión con RabbitMQ
        connection = connect_to_rabbitmq()
        channel = connection.channel()

        #Se define la cola
        channel.queue_declare(queue="notificaciones.enviadas", durable=False)

        #Se publica el mensaje en la cola
        publish_message(channel, "notificaciones.enviadas", message)

        #Se cierra la conexión
        connection.close()
        print("Mensaje enviado con éxito al productor RabbitMQ.")

    except Exception as e:
        print(f"Error al enviar el mensaje al productor: {str(e)}")
