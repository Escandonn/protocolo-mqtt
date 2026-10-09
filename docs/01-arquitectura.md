# Arquitectura del Sistema

Este proyecto demuestra una arquitectura de tres componentes comunicándose mediante dos protocolos diferentes.

## Estructura del Proyecto

```text
fastapi-mqtt-example/
│
├── backend/
│   ├── __init__.py
│   ├── main.py          # FastAPI con endpoint POST /mqtt/publicar
│   └── mqtt_client.py   # Cliente MQTT (paho-mqtt) para publicar
│
├── mqtt-frontend/
│   └── subscriber.py    # Suscriptor MQTT que imprime con print()
│
├── docs/
└── requirements.txt
```

## Arquitectura General

```text
HTTP
 │
 ▼
 FastAPI (backend/)
 │
 │ MQTT Publish
 ▼
 MQTT Broker
 │
 │ MQTT Subscribe
 ▼
 Python Subscriber (mqtt-frontend/)
 │
 ▼
 print()
```

## Componentes

### 1. Cliente HTTP
- Cualquier herramienta que pueda hacer peticiones HTTP (curl, Postman, navegador)
- Envía peticiones POST a FastAPI

### 2. FastAPI (backend/main.py)
- Framework web para crear APIs REST
- Expone el endpoint `POST /mqtt/publicar`
- Actúa como **Publisher MQTT**: recibe HTTP y publica en MQTT

### 3. MQTT Client (backend/mqtt_client.py)
- Módulo que encapsula la lógica de publicación MQTT
- Usa la librería `paho-mqtt`
- Función principal: `publish_message(message)`

### 4. MQTT Broker (Mosquitto)
- Servidor central de mensajería
- Recibe mensajes de publishers y los entrega a subscribers
- No guarda estado de los clientes (salvo sesiones persistentes)

### 5. Python Subscriber (mqtt-frontend/subscriber.py)
- Programa independiente que se conecta al broker
- Se suscribe al topic `demo/mensagem`
- Actúa como **Subscriber MQTT**: recibe mensajes y los imprime

## Responsabilidad de Cada Componente

| Componente | Responsabilidad |
|------------|-----------------|
| Cliente HTTP | Iniciar la comunicación enviando datos |
| FastAPI | Exponer API REST, validar entrada, orquestar publicación MQTT |
| mqtt_client.py | Manejar conexión y publicación hacia el broker |
| Mosquitto | Recibir, enrutar y entregar mensajes por topic |
| subscriber.py | Escuchar mensajes y procesarlos (imprimir) |

## Flujo de Información

```
1. Cliente HTTP → POST /mqtt/publicar {"mensaje": "Hola"}
                    │
                    ▼
2. FastAPI valida JSON y llama publish_message("Hola")
                    │
                    ▼
3. mqtt_client.py conecta a localhost:1883
                    │
                    ▼
4. Publica en topic "demo/mensagem"
                    │
                    ▼
5. Mosquitto recibe y ve suscriptores en "demo/mensagem"
                    │
                    ▼
6. Entrega mensaje a subscriber.py
                    │
                    ▼
7. subscriber.py ejecuta print("Nuevo mensaje recibido: Hola")
```

## Por Qué FastAPI Está Separado de MQTT

FastAPI es un framework **HTTP** (request/response síncrono).
MQTT es un protocolo **publish/subscribe** (asíncrono, desacoplado).

Separarlos permite:
- Entender claramente cada protocolo
- Cambiar el broker sin tocar FastAPI
- Tener múltiples subscribers sin modificar el publisher
- Escalar independientemente cada parte

## Diagrama ASCII Completo

```text
┌─────────────┐     HTTP POST      ┌──────────┐
│   Cliente   │ ─────────────────> │          │
│   (curl)    │                    │ FastAPI  │
└─────────────┘                    │          │
                                   └────┬─────┘
                                        │ publish_message()
                                        ▼
                              ┌─────────────────┐
                              │  mqtt_client.py │
                              │  (paho-mqtt)    │
                              └────────┬────────┘
                                       │ MQTT PUBLISH
                                       ▼
                              ┌─────────────────┐
                              │  MQTT Broker    │
                              │   (Mosquitto)   │
                              │  localhost:1883 │
                              └────────┬────────┘
                                       │ MQTT SUBSCRIBE
                                       ▼
                              ┌─────────────────┐
                              │ subscriber.py   │
                              │ (paho-mqtt)     │
                              └────────┬────────┘
                                       │ on_message()
                                       ▼
                              ┌─────────────────┐
                              │   print()       │
                              └─────────────────┘
```