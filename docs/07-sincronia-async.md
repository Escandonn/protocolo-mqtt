# Flujo Síncrono vs Asíncrono

## Flujo Actual (Síncrono por HTTP, Asíncrono por MQTT)

```text
Frontend (React/Astro)
   │
   │ HTTP POST /mqtt/publicar
   ▼
Backend (FastAPI)
   │
   │ publish_message()
   ▼
MQTT Broker (Mosquitto)
   │
   │ Entrega inmediata
   ▼
Subscriber (mqtt-frontend/subscriber.py)
   │
   │ on_message() callback
   ▼
print("Nuevo mensaje recibido: ...")
```

## ¿Es Síncrono o Asíncrono?

**Depende de la capa:**

| Capa | Tipo | Explicación |
|------|------|-------------|
| Frontend → Backend | **Síncrono** | `fetch()` espera la respuesta HTTP |
| Backend → MQTT Broker | **Síncrono** | `publish()` espera confirmación (QoS 0 = fire-and-forget) |
| MQTT Broker → Subscriber | **Asíncrono** | El broker empuja el mensaje cuando llegue |

## ¿Por qué el Frontend no ve el print()?

El **Frontend solo recibe la respuesta HTTP** de FastAPI. El `print()` ocurre en el **Subscriber**, que es un proceso Python separado.

Para ver el print() en el frontend, se necesitaría:
1. El subscriber publicando de vuelta a otro topic
2. El frontend suscribiéndose a MQTT vía WebSocket
3. O un endpoint HTTP que el subscriber actualice

## Posibles Mejoras (no implementadas)

### Opción A: Subscriber → Backend → Frontend
```text
Subscriber recibe → publica en "demo/ack" → Backend se suscribe → endpoint /ultimo-mensagem → Frontend consulta
```

### Opción B: MQTT vía WebSocket
```text
Frontend se suscribe directamente al broker usando MQTT over WebSocket
```

## Cómo Cambió el Frontend

**Antes:** Solo un botón que hacía `fetch` y mostraba `alert()`.

**Ahora:** 
- Botón con estado de carga (deshabilitado + gris)
- Texto de feedback en tiempo real
- Colores: azul (esperando) → verde (éxito) → rojo (error)
- Restauración automática después de 3 segundos

**Código clave en `index.astro`:**
```javascript
btn.addEventListener('click', async () => {
  btn.disabled = true;  // Desactivar botón
  estado.textContent = 'Enviando a FastAPI...';
  
  const data = await fetch(...);
  
  if (data.status === 'ok') {
    estado.textContent = '✓ Mensaje enviado a MQTT Broker → Subscriber lo recibe';
    estado.style.color = '#28a745';
  }
});
```

## Transición Visual por Paso

1. **Click botón** → Botón se vuelve gris y se desactiva
2. **HTTP POST** → Texto: "Enviando a FastAPI..." (azul)
3. **FastAPI publica MQTT** → Broker recibe
4. **Respuesta HTTP** → Texto: "✓ Mensaje enviado..." (verde)
5. **3 segundos después** → Botón se restaura

El subscriber (terminal separada) muestra:
```
Nuevo mensaje recibido: Hola desde el frontend
```

## Código Completo del Backend (actualizado)

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
```

La respuesta incluye `timestamp` para que el frontend pueda mostrar cuándo se envió.