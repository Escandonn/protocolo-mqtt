
**Python → FastAPI → MQTT Broker → Python (`print`)**

La segunda aplicación Python actuará como receptor MQTT y mostrará los mensajes con `print()`.

Aquí tienes un prompt listo para copiar en otra IA:

Quiero que desarrolles un proyecto educativo MUY BÁSICO para demostrar la comunicación entre **FastAPI, MQTT y Python**.

## Objetivo

Crear un ejemplo funcional donde:

```text
Cliente HTTP
     │
     ▼
 FastAPI
     │
     │ MQTT
     ▼
 MQTT Broker
     │
     │ MQTT
     ▼
Python Subscriber
     │
     ▼
  print()
```

El objetivo es comprender de forma sencilla:

* Qué hace FastAPI.
* Qué hace MQTT.
* Qué hace un MQTT Broker.
* Cómo Python publica mensajes MQTT.
* Cómo Python recibe mensajes MQTT.
* Cómo FastAPI puede utilizar MQTT.
* Diferencia entre HTTP y MQTT.
* Conceptos de `publish` y `subscribe`.
* Concepto de `topic`.

No quiero React, ESP32, sensores, bases de datos, Docker ni arquitecturas complejas.

Debe ser un proyecto pequeño y fácil de ejecutar localmente.

---

# 1. Tecnologías

Utiliza:

* Python 3.11+
* FastAPI
* Uvicorn
* Paho MQTT
* Mosquitto como MQTT Broker

Instalación:

```bash
pip install fastapi uvicorn paho-mqtt
```

Explica también cómo instalar Mosquitto en Windows.

---

# 2. Estructura del proyecto

Crea esta estructura:

```text
fastapi-mqtt-example/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   └── mqtt_client.py
│
├── subscriber/
│   └── subscriber.py
│
├── docs/
│   ├── 01-arquitectura.md
│   ├── 02-fastapi.md
│   ├── 03-mqtt.md
│   ├── 04-topicos.md
│   ├── 05-flujo-comunicacion.md
│   └── 06-ejecucion.md
│
├── requirements.txt
└── README.md
```

---

# 3. FastAPI

Crear un endpoint:

```http
POST /mqtt/publicar
```

Debe recibir un JSON como:

```json
{
    "mensaje": "Hola desde FastAPI"
}
```

Cuando FastAPI reciba la petición, debe publicar el mensaje en MQTT.

Utilizar este topic:

```text
demo/mensaje
```

Ejemplo conceptual:

```text
POST /mqtt/publicar
        │
        ▼
     FastAPI
        │
        ▼
mqtt_client.publish()
        │
        ▼
MQTT Broker
```

La respuesta de FastAPI debe ser sencilla:

```json
{
    "status": "ok",
    "mensaje": "Hola desde FastAPI"
}
```

---

# 4. Cliente MQTT de FastAPI

Crear:

```text
app/mqtt_client.py
```

Utilizar la librería:

```python
paho-mqtt
```

Configurar inicialmente:

```text
BROKER = "localhost"
PORT = 1883
TOPIC = "demo/mensaje"
```

Crear una función sencilla:

```python
publish_message(message)
```

Esta función debe conectarse al broker y publicar el mensaje.

Mantén el código lo más sencillo posible para fines educativos.

---

# 5. Subscriber Python

Crear:

```text
subscriber/subscriber.py
```

Este programa debe conectarse al MQTT Broker y suscribirse:

```text
demo/mensaje
```

Cuando llegue un mensaje debe ejecutar:

```python
print(...)
```

Ejemplo:

```text
Mensaje recibido:
Hola desde FastAPI
```

El subscriber debe permanecer escuchando mensajes.

Conceptualmente:

```text
MQTT Broker
     │
     │ demo/mensaje
     ▼
subscriber.py
     │
     ▼
print()
```

---

# 6. Ejemplo completo

El proyecto debe permitir realizar:

```text
1. Ejecutar Mosquitto

2. Ejecutar subscriber.py

3. Ejecutar FastAPI

4. Enviar POST a FastAPI

5. FastAPI publica mediante MQTT

6. MQTT Broker entrega el mensaje

7. subscriber.py recibe el mensaje

8. Python muestra el mensaje con print()
```

Ejemplo de petición:

```bash
curl -X POST http://127.0.0.1:8000/mqtt/publicar ^
-H "Content-Type: application/json" ^
-d "{\"mensaje\":\"Hola MQTT\"}"
```

El resultado esperado en `subscriber.py`:

```text
Mensaje recibido: Hola MQTT
```

---

# 7. README.md

Crear un README completo pero sencillo que explique:

## Nombre

FastAPI + MQTT + Python

## Descripción

Una demostración mínima de comunicación entre una API REST desarrollada con FastAPI y un broker MQTT utilizando Python.

## Arquitectura

Incluir un diagrama ASCII:

```text
HTTP
 │
 ▼
FastAPI
 │
 │ MQTT Publish
 ▼
MQTT Broker
 │
 │ MQTT Subscribe
 ▼
Python Subscriber
 │
 ▼
print()
```

## Instalación

Explicar paso a paso:

1. Instalar Python.
2. Crear entorno virtual.
3. Activar entorno virtual.
4. Instalar dependencias.
5. Instalar Mosquitto.
6. Ejecutar Mosquitto.
7. Ejecutar subscriber.
8. Ejecutar FastAPI.
9. Realizar una petición.

---

# 8. Documentación Markdown

Crear varios documentos `.md`.

## docs/01-arquitectura.md

Explicar:

* arquitectura inicial;
* componentes;
* responsabilidad de cada componente;
* flujo de información;
* por qué FastAPI está separado de MQTT;
* diagrama ASCII.

---

## docs/02-fastapi.md

Explicar:

* qué es FastAPI;
* qué es un endpoint;
* qué es HTTP;
* qué hace el endpoint `/mqtt/publicar`;
* ejemplo de petición;
* ejemplo de respuesta.

---

## docs/03-mqtt.md

Explicar de manera sencilla:

* qué es MQTT;
* qué es un Broker;
* qué es Publisher;
* qué es Subscriber;
* qué es un Topic;
* qué significa `publish`;
* qué significa `subscribe`.

Incluir un ejemplo:

```text
Publisher
   │
   │ publish
   ▼
Broker
   │
   │ subscribe
   ▼
Subscriber
```

---

## docs/04-topicos.md

Explicar qué es un MQTT Topic.

Utilizar:

```text
demo/mensaje
```

Explicar:

```text
demo
└── mensaje
```

Mostrar cómo el publisher publica:

```text
demo/mensaje
```

Y cómo el subscriber se suscribe:

```text
demo/mensaje
```

---

## docs/05-flujo-comunicacion.md

Explicar detalladamente este flujo:

```text
Cliente
   │
   │ HTTP POST
   ▼
FastAPI
   │
   │ publish
   ▼
MQTT Broker
   │
   │ mensaje
   ▼
Python Subscriber
   │
   │ callback
   ▼
print()
```

Explicar qué ocurre en cada paso.

---

## docs/06-ejecucion.md

Crear una guía práctica desde cero para Windows.

Debe explicar exactamente qué terminal abrir y qué comando ejecutar.

Por ejemplo:

### Terminal 1

```bash
mosquitto
```

### Terminal 2

```bash
python subscriber/subscriber.py
```

### Terminal 3

```bash
uvicorn app.main:app --reload
```

Después realizar una petición HTTP.

Mostrar el resultado esperado.

---

# 9. requirements.txt

Crear:

```text
fastapi
uvicorn
paho-mqtt
```

---

# 10. Reglas importantes

No agregues:

* React.
* ESP32.
* WebSockets.
* Redis.
* Celery.
* Docker.
* Kubernetes.
* PostgreSQL.
* autenticación.
* JWT.
* microservicios.
* bases de datos.
* frontend.
* sensores.

El proyecto debe ser **intencionalmente pequeño**.

No quiero solamente fragmentos de código.

Quiero que entregues:

1. La estructura completa del proyecto.
2. Todos los archivos.
3. Código completo de cada archivo.
4. Explicación de cada archivo.
5. Comandos de instalación.
6. Comandos de ejecución.
7. Ejemplo de prueba.
8. Resultado esperado.
9. Documentación `.md`.
10. README.md.

El código debe estar diseñado para que una persona que está aprendiendo **FastAPI + MQTT** pueda entenderlo línea por línea.

Primero debe funcionar el ejemplo básico y posteriormente se pueden proponer posibles mejoras, pero NO implementarlas en esta primera versión.

**La arquitectura queda deliberadamente sencilla:** FastAPI no se comunica directamente con el `subscriber`; ambos pasan por el **Broker MQTT**. Esto permite entender claramente el patrón **publish/subscribe** antes de agregar ESP32, React u otros componentes.
