import grpc
import notification_pb2
import notification_pb2_grpc

def run():
    # Conectarse al servidor gRPC
    channel = grpc.insecure_channel('localhost:50051')
    stub = notification_pb2_grpc.NotificationServiceStub(channel)

    # Crear una solicitud para enviar
    request = notification_pb2.SendNotificationRequest(
        usuarioId="550e8400-e29b-41d4-a716-446655440001",
        mensaje="Mensaje de prueba gRPC",
        tipo="email"
    )

    # Llamar al servicio gRPC
    response = stub.SendNotification(request)
    print(f"Notificación recibida: {response}")

if __name__ == "__main__":
    run()
