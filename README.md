# FastAPI + MQTT + Python

Una demostración mínima de comunicación entre una API REST desarrollada con FastAPI, un broker MQTT (Mosquitto) y un frontend web (Astro).

## Estructura del proyecto

```text
protoocolo-mqtt/
│
├── backend/
│   ├── __init__.py
│   ├── main.py          # FastAPI con endpoint POST /mqtt/publicar
│   └── mqtt_client.py   # MQTT publisher (paho-mqtt)
│
├── mqtt-frontend/
│   └── subscriber.py    # MQTT subscriber → print()
│
├── frontend-astro-react/
│   └── src/pages/
│       └── index.astro  # Botón central con feedback visual
│
├── docs/
│   ├── 01-arquitectura.md
│   ├── 02-fastapi.md
│   ├── 03-mqtt.md
│   ├── 04-topicos.md
│   ├── 05-flujo-comunicacion.md
│   ├── 06-ejecucion.md
│   └── 07-sincronia-async.md
│
├── requirements.txt
└── README.md
```

## Arquitectura

```text
Frontend (Astro)
   │
   │ HTTP POST /mqtt/publicar
   ▼
Backend (FastAPI)
   │
   │ publish_message()
   ▼
MQTT Broker (Mosquitto)
   │
   │ entrega a suscriptores
   ▼
Subscriber (mqtt-frontend/subscriber.py)
   │
   │ on_message() callback
   ▼
print("Nuevo mensaje recibido: ...")
```

## Instalación

### 1. Instalar Python
Descarga e instala Python 3.11+ desde [python.org](https://www.python.org/downloads/).

### 2. Crear entorno virtual
```bash
python -m venv venv
```

### 3. Activar entorno virtual
```bash
# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

### 4. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 5. Instalar Mosquitto (Windows)
1. Descarga el instalador desde [mosquitto.org/download](https://mosquitto.org/download/)
2. Ejecuta el `.exe` y sigue los pasos
3. Asegúrate de que el servicio Mosquitto esté ejecutándose

> **Nota:** En Windows, Mosquitto se instala como servicio. Para verificarlo:
> ```bash
> net start mosquitto
> ```
> O ejecuta manualmente en una terminal: `mosquitto`

## Ejecución (4 terminales)

### Terminal 1: Mosquitto
```bash
mosquitto -v
```

### Terminal 2: Subscriber
```bash
cd mqtt-frontend
python subscriber.py
```

### Terminal 3: FastAPI
```bash
cd backend
uvicorn main:app --reload
```

### Terminal 4: Frontend web
```bash
cd frontend-astro-react
npm install
astro dev --background
```

Abre `http://localhost:4321` y haz click en el botón.

## Resultado esperado

**En el navegador (frontend):**
```text
✓ Mensaje enviado a MQTT Broker → Subscriber lo recibe
```

**En la terminal del subscriber:**
```text
Nuevo mensaje recibido: Hola desde el frontend
```

**En la respuesta HTTP:**
```json
{
  "status": "ok",
  "mensagem": "Hola desde el frontend",
  "timestamp": "2025-01-15T10:30:00.123456",
  "topic": "demo/mensagem",
  "broker": "localhost:1883"
}
```

## Documentación

- [Arquitectura](docs/01-arquitectura.md)
- [FastAPI](docs/02-fastapi.md)
- [MQTT](docs/03-mqtt.md)
- [Tópicos](docs/04-topicos.md)
- [Flujo de comunicación](docs/05-flujo-comunicacion.md)
- [Guía de ejecución](docs/06-ejecucion.md)
- [Síncrono vs Asíncrono](docs/07-sincronia-async.md)

## Conceptos clave

| Concepto | Descripción |
|----------|-------------|
| **FastAPI** | Framework web moderno para APIs REST |
| **MQTT** | Protocolo ligero de mensajería publish/subscribe |
| **Broker** | Servidor central que recibe y distribuye mensajes |
| **Publisher** | Cliente que envía mensajes (FastAPI) |
| **Subscriber** | Cliente que recibe mensajes (subscriber.py) |
| **Topic** | Canal de comunicación (ej: `demo/mensagem`) |
| **Frontend** | Página web con un botón (Astro) |

## Diferencia HTTP vs MQTT

| HTTP | MQTT |
|------|------|
| Request/Response | Publish/Subscribe |
| Cliente-Servidor | Desacoplado via Broker |
| Síncrono | Asíncrono |
| Una conexión por petición | Conexión persistente |

## Licencia

MIT