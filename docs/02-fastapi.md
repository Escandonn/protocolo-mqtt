# FastAPI

## Qué es FastAPI

FastAPI es un framework web moderno y rápido para construir APIs con Python 3.7+.
Se basa en:
- **Starlette** para la parte web
- **Pydantic** para validación de datos
- **Type hints** de Python para documentación automática

## Qué es un Endpoint

Un endpoint es una URL específica en la API que realiza una acción.
En FastAPI se define con decoradores:

```python
@app.post("/mqtt/publicar")
async def publicar_mensagem(request: MensajeRequest):
    ...
```

## Qué es HTTP

HTTP (HyperText Transfer Protocol) es el protocolo de la web.
Funciona en modelo **Request/Response**:
1. Cliente envía **Request** (petición)
2. Servidor procesa y devuelve **Response** ( respuesta)

Es **síncrono**: el cliente espera la respuesta.

## Qué Hace el Endpoint `/mqtt/publicar`

Este endpoint:
1. Recibe una petición POST con JSON
2. Valida que tenga el campo `mensaje` (string)
3. Llama a `publish_message()` para enviarlo por MQTT
4. Retorna confirmación JSON con timestamp

**No conoce al subscriber** - solo publica en el broker.

## Ejemplo de Petición

```bash
curl -X POST http://127.0.0.1:8000/mqtt/publicar \
-H "Content-Type: application/json" \
-d "{\"mensaje\":\"Hola desde FastAPI\"}"
```

**Body JSON:**
```json
{
    "mensaje": "Hola desde FastAPI"
}
```

## Ejemplo de Respuesta

**Éxito:**
```json
{
    "status": "ok",
    "mensaje": "Hola desde FastAPI",
    "timestamp": "2025-01-15T10:30:00.123456",
    "topic": "demo/mensagem",
    "broker": "localhost:1883"
}
```

**Error (si falla MQTT):**
```json
{
    "status": "error",
    "mensaje": "Hola desde FastAPI",
    "timestamp": "2025-01-15T10:30:00.123456",
    "topic": "demo/mensagem",
    "broker": "localhost:1883"
}
```

## Código Completo (backend/main.py)

```python
from fastapi import FastAPI
from pydantic import BaseModel
from mqtt_client import publish_message
from datetime import datetime

app = FastAPI(title="FastAPI MQTT Demo")

class MensagemRequest(BaseModel):
    mensagem: str

@app.post("/mqtt/publicar")
async def publicar_mensagem(request: MensagemRequest):
    timestamp = datetime.now().isoformat()
    exito = publish_message(request.mensagem)
    return {
        "status": "ok" if exito else "error",
        "mensagem": request.mensagem,
        "timestamp": timestamp,
        "topic": "demo/mensagem",
        "broker": "localhost:1883"
    }

@app.get("/")
async def root():
    return {
        "message": "FastAPI MQTT Demo",
        "endpoints": {
            "publicar": "POST /mqtt/publicar",
            "documentacao": "/docs"
        }
    }
```

## Puntos Clave para Aprender

1. **Pydantic Model**: `MensagemRequest` valida automáticamente el JSON
2. **Type hints**: `request: MensagemRequest` da autocompletado y docs
3. **Async**: `async def` permite manejar múltiples peticiones
4. **Separación**: La lógica MQTT está en `mqtt_client.py`, no aquí
5. **Timestamp**: Incluye hora real de envío para debugging
6. **Frontend**: El botón en Astro llama a este endpoint