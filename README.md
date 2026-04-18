# 🐇 Actividad en Clase — RabbitMQ

<div align="center">

![RabbitMQ](https://img.shields.io/badge/RabbitMQ-FF6600?style=for-the-badge&logo=rabbitmq&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)
![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)

**Sistemas Distribuidos — COTECNOVA**
**Clase 9: Colas y Comunicación Asíncrona**

</div>

---

##  Integrantes

| Nombre |
|--------|
| Esteban Murillo Gómez |
| Miguel Ángel Villamil Echavarria |
| Rooger Andrés Gómez |
| Mauricio López Campiño |

**Docente:** Jhon James Cano Sánchez
**Asignatura:** Sistemas Distribuidos

---

##  Descripción

En esta actividad implementamos un sistema básico de mensajería asíncrona usando **RabbitMQ** como broker de mensajes. El objetivo fue entender el concepto de **desacoplamiento** entre servicios a través de colas, pasando de la comunicación directa HTTP a una comunicación asíncrona con colas.

### ¿Por qué RabbitMQ?

Anteriormente trabajamos con comunicación directa (HTTP), lo cual tiene problemas:
- Si el servicio B falla → el servicio A también falla
- Acoplamiento fuerte entre servicios
- No escala bien
- Genera espera bloqueante

Con **RabbitMQ** resolvemos esto así:

```
Servicio A → COLA → Servicio B
```

---

##  Arquitectura

```
┌─────────────┐        ┌──────────────────┐        ┌─────────────────┐
│  producer.py │──────▶│    RabbitMQ       │──────▶│  consumer.py    │
│              │        │  cola: 'citas'    │        │                 │
│  Envía msg   │        │  (broker)         │        │  Recibe msg     │
└─────────────┘        └──────────────────┘        └─────────────────┘
```

### Conceptos clave

| Componente | Rol | Comando |
|------------|-----|---------|
| `producer.py` | Envía mensajes a la cola | `python producer.py` |
| `consumer.py` | Escucha y procesa mensajes | `python consumer.py` |
| **RabbitMQ** | Intermediario (broker) | Servicio Docker activo |

---

##  Stack Tecnológico

- **RabbitMQ 3** — Broker de mensajes
- **Python 3** — Lenguaje de programación
- **pika** — Librería Python para conectarse a RabbitMQ
- **Docker Desktop** — Para correr RabbitMQ en Windows sin WSL

---

##  Instalación y configuración

### 1. Levantar RabbitMQ con Docker

```bash
docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
```

Verificar que está corriendo:

```bash
docker ps
```

Panel de administración web: [http://localhost:15672](http://localhost:15672)
> Usuario: `guest` | Contraseña: `guest`

### 2. Preparar entorno Python

```bash
mkdir rabbitmq-clase9
cd rabbitmq-clase9
python -m venv venv
venv\Scripts\activate
pip install pika
```

---

##  Código

### `producer.py` — Envía mensajes

```python
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
```

### `consumer.py` — Recibe mensajes

```python
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
```

---

##  Ejecución

Se necesitan **dos terminales** abiertas con el entorno virtual activo:

**Terminal 1 — Consumer (arranca primero):**
```bash
python consumer.py
```
Resultado esperado:
```
Esperando mensajes...
```

**Terminal 2 — Producer:**
```bash
python producer.py
```
Resultado:
```
Mensaje enviado a la cola
```

**Resultado final en Terminal 1:**
```
Mensaje recibido: Nueva cita creada
```

---

## 📊 Redis vs RabbitMQ

| | Redis | RabbitMQ |
|---|---|---|
| **Rol** | Coordinación | Mensajería |
| **Usa** | Locks | Colas |
| **Para** | Estado compartido | Comunicación asíncrona |

> Redis controla el acceso — RabbitMQ gestiona la comunicación.

---

##  Estructura del proyecto

```
rabbitmq-clase9/
├── venv/               # Entorno virtual Python
├── producer.py         # Envía mensajes a la cola
├── consumer.py         # Escucha y procesa mensajes
└── README.md           
```

---

<div align="center">

**COTECNOVA — Sistemas Distribuidos 2026**

![RabbitMQ](https://img.shields.io/badge/Clase_9-RabbitMQ-FF6600?style=flat-square&logo=rabbitmq&logoColor=white)
![Status](https://img.shields.io/badge/Actividad_en_clase-✅_Completada-success?style=flat-square)

</div>