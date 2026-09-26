# MQTT

## Qué es MQTT

MQTT (Message Queuing Telemetry Transport) es un protocolo de mensajería **ligero** diseñado para:
- Redes inestables
- Dispositivos con pocos recursos
- Comunicación **publish/subscribe**

## Qué es un Broker

El **Broker** es el servidor central. Sus funciones:
1. Recibe mensajes de los **Publishers**
2. Filtra por **Topic**
3. Entrega a los **Subscriptores** interesados

**El broker NO conoce la lógica de negocio** - solo enruta mensajes.

Ejemplos de brokers: Mosquitto, EMQX, HiveMQ, VerneMQ.

## Qué es Publisher

Un **Publisher** (publicador) es un cliente que:
- Se conecta al broker
- Envía (publica) mensajes en un **topic**
- No sabe quién recibe el mensaje
- No espera respuesta

En este proyecto: **FastAPI (vía mqtt_client.py)** es el publisher.

## Qué es Subscriber

Un **Subscriber** (suscriptor) es un cliente que:
- Se conecta al broker
- Se suscribe a uno o más **topics**
- Recibe mensajes cuando llegan
- Procesa los mensajes (callback)

En este proyecto: **subscriber.py** es el subscriber.

## Qué es un Topic

Un **Topic** es un string que actúa como **canal de comunicación**.
Ejemplo: `demo/mensaje`

Características:
- Jerárquico con `/` (como carpetas)
- Case-sensitive
- El publisher publica EN un topic
- El subscriber se suscribe A un topic

## Qué Significa `publish`

**Publicar** = enviar un mensaje al broker en un topic específico.

```python
client.publish("demo/mensaje", "Hola MQTT")
```

El broker recibe el mensaje y lo entrega a todos los suscriptores de ese topic.

## Qué Significa `subscribe`

**Suscribirse** = decirle al broker: "Quiero recibir todos los mensajes de este topic".

```python
client.subscribe("demo/mensaje")
```

A partir de ese momento, el callback `on_message` se ejecutará al llegar mensajes.

## Diagrama Conceptual

```text
Publisher
   │
   │ publish("demo/mensaje", "Hola")
   ▼
Broker
   │
   │ entrega a suscriptores de "demo/mensaje"
   ▼
Subscriber
   │
   │ on_message() callback
   ▼
Procesa mensaje
```

## Características Clave de MQTT

| Característica | Descripción |
|----------------|-------------|
| **Desacoplado** | Publisher y subscriber no se conocen |
| **Asíncrono** | No hay request/response directo |
| **Ligero** | Header mínimo (2 bytes) |
| **QoS** | 3 niveles de garantía de entrega |
| **Retained** | Último mensaje guardado para nuevos suscriptores |
| **Last Will** | Mensaje automático si cliente se desconecta |

## En Este Proyecto

- **Broker**: Mosquitto en `localhost:1883`
- **Topic**: `demo/mensaje`
- **Publisher**: `app/mqtt_client.py` → `publish_message()`
- **Subscriber**: `subscriber/subscriber.py` → `on_message()`
- **QoS**: 0 (fire and forget, por simplicidad)