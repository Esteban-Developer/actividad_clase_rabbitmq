import pika  # Librería para conectarse a RabbitMQ

# Crear conexión con el servidor RabbitMQ
connection = pika.BlockingConnection(
    pika.ConnectionParameters('localhost')
)

# Crear canal de comunicación
channel = connection.channel()

# Crear cola llamada 'citas' (si no existe)
channel.queue_declare(queue='citas')

# Enviar mensaje
channel.basic_publish(
    exchange='',
    routing_key='citas',
    body='Nueva cita creada'
)

print("Mensaje enviado a la cola")

# Cerrar conexión
connection.close()