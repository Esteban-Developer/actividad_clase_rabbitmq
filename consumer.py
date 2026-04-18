import pika  # Librería para RabbitMQ

# Conectar con RabbitMQ
connection = pika.BlockingConnection(
    pika.ConnectionParameters('localhost')
)

# Crear canal
channel = connection.channel()

# Asegurar que la cola existe
channel.queue_declare(queue='citas')

# Función que se ejecuta cuando llega un mensaje
def callback(ch, method, properties, body):
    print("Mensaje recibido:", body.decode())

# Indicar que escuche la cola
channel.basic_consume(
    queue='citas',
    on_message_callback=callback,
    auto_ack=True
)

print("Esperando mensajes...")

# Mantener el proceso activo escuchando
channel.start_consuming()