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
async def publicar_mensaje(request: MensajeRequest):
    ...
```

## Qué es HTTP

HTTP (HyperText Transfer Protocol) es el protocolo de la web.
Funciona en modelo **Request/Response**:
1. Cliente envía **Request** (petición)
2. Servidor procesa y devuelve **Response** (respuesta)

Es **síncrono**: el cliente espera la respuesta.

## Qué Hace el Endpoint `/mqtt/publicar`

Este endpoint:
1. Recibe una petición POST con JSON
2. Valida que tenga el campo `mensaje` (string)
3. Llama a `publish_message()` para enviarlo por MQTT
4. Retorna confirmación JSON

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
    "mensaje": "Hola desde FastAPI"
}
```

**Error (si falla MQTT):**
```json
{
    "status": "error",
    "mensaje": "Hola desde FastAPI"
}
```

## Código Completo (app/main.py)

```python
from fastapi import FastAPI
from pydantic import BaseModel
from app.mqtt_client import publish_message

app = FastAPI(title="FastAPI MQTT Demo")

class MensajeRequest(BaseModel):
    mensaje: str

@app.post("/mqtt/publicar")
async def publicar_mensaje(request: MensajeRequest):
    exito = publish_message(request.mensaje)
    return {
        "status": "ok" if exito else "error",
        "mensaje": request.mensaje
    }

@app.get("/")
async def root():
    return {"message": "FastAPI MQTT Demo - Usa POST /mqtt/publicar"}
```

## Puntos Clave para Aprender

1. **Pydantic Model**: `MensajeRequest` valida automáticamente el JSON
2. **Type hints**: `request: MensajeRequest` da autocompletado y docs
3. **Async**: `async def` permite manejar múltiples peticiones
4. **Separación**: La lógica MQTT está en `mqtt_client.py`, no aquí
5. **Respuesta simple**: Solo confirma recepción, no espera al subscriber