# Flujo de Comunicación

## Flujo Completo

```text
Frontend (Astro)
   │
   │ HTTP POST /mqtt/publicar {"mensagem": "Hola"}
   ▼
Backend (FastAPI)
   │
   │ publish_message("Hola")
   ▼
MQTT Broker
   │
   │ mensagem "Hola" en topic "demo/mensagem"
   ▼
Subscriber (mqtt-frontend/subscriber.py)
   │
   │ callback on_message()
   ▼
print("Nuevo mensaje recibido: Hola")
```

## Explicación Paso a Paso

### Paso 1: Frontend → Backend (HTTP)

**Qué ocurre:**
- Usuario hace click en el botón del frontend (Astro)
- Se envía petición POST a `http://127.0.0.1:8000/mqtt/publicar`
- Headers: `Content-Type: application/json`
- Body: `{"mensagem": "Hola desde el frontend"}`

**Protocolo:** HTTP/1.1 (Request/Response)
**Puerto:** 8000 (FastAPI/Uvicorn)

**Código en el frontend:**
```javascript
const response = await fetch('http://127.0.0.1:8000/mqtt/publicar', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ mensagem: 'Hola desde el frontend' })
});
```

---

### Paso 2: Backend Valida y Procesa

**Qué ocurre en `backend/main.py`:**
1. FastAPI recibe la petición
2. Pydantic valida el JSON contra `MensagemRequest`
3. Si es válido, extrae `request.mensagem`
4. Llama a `publish_message(request.mensagem)`
5. Retorna JSON con timestamp

**Código:**
```python
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

**Importante:** FastAPI **no espera** al subscriber. Retorna inmediato.

---

### Paso 3: Backend → MQTT Broker (Publish)

**Qué ocurre en `backend/mqtt_client.py`:**
1. Crea cliente MQTT nuevo
2. Conecta a `localhost:1883`
3. Ejecuta `client.publish("demo/mensagem", "Hola MQTT")`
4. Desconecta

**Protocolo:** MQTT 3.1.1 / 5.0
**Puerto:** 1883
**QoS:** 0 (máximo una vez, sin confirmación)

**Código:**
```python
def publish_message(message: str):
    client = mqtt.Client()
    client.connect(BROKER, PORT, 60)
    result = client.publish(TOPIC, message)
    client.disconnect()
    return result.rc == mqtt.MQTT_ERR_SUCCESS
```

---

### Paso 4: MQTT Broker Recibe y Enruta

**Qué ocurre en Mosquitto:**
1. Recibe paquete PUBLISH en topic `demo/mensagem`
2. Busca en su tabla de suscripciones
3. Encuentra a `subscriber.py` suscrito a `demo/mensagem`
4. Reenvía el mensaje al subscriber

**El broker NO modifica el mensaje** - solo lo entrega.

---

### Paso 5: MQTT Broker → Subscriber (Entrega)

**Qué ocurre:**
- Broker envía paquete PUBLISH al subscriber conectado
- El mensaje viaja por la conexión TCP persistente
- Llega al callback `on_message` del cliente paho-mqtt

---

### Paso 6: Subscriber Procesa (Callback)

**Qué ocurre en `mqtt-frontend/subscriber.py`:**
1. Se ejecuta `on_message(client, userdata, msg)`
2. `msg.payload` contiene los bytes del mensaje
3. Decodifica: `msg.payload.decode()` → `"Hola MQTT"`
4. Ejecuta `print(f"\nNuevo mensaje recibido: {mensagem}")`

**Código:**
```python
def on_message(client, userdata, msg):
    mensagem = msg.payload.decode()
    print(f"\nNuevo mensaje recibido: {mensagem}")
```

---

### Paso 7: Frontend Recibe Respuesta HTTP

**Qué ocurre en el frontend:**
1. `await response.json()` recibe la respuesta
2. Si `data.status === 'ok'`: muestra verde "✓ Mensaje enviado..."
3. Si error: muestra rojo "✗ Error: ..."
4. Botón se desactiva 3 segundos

**Código en el frontend:**
```javascript
if (response.ok && data.status === 'ok') {
  estado.textContent = '✓ Mensaje enviado a MQTT Broker → Subscriber lo recibe';
  estado.style.color = '#28a745';
}
```

---

### Paso 8: Resultado Visible

**En el Frontend (navegador):**
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

## Resumen de Protocolos y Puertos

| Tramo | Protocolo | Puerto | Dirección |
|-------|-----------|--------|-----------|
| Frontend → Backend | HTTP | 8000 | Request/Response |
| Backend → Broker | MQTT | 1883 | Publish |
| Broker → Subscriber | MQTT | 1883 | Push (async) |

## Puntos Clave para Entender

1. **Desacoplamiento**: Frontend no conoce a subscriber, subscriber no conoce a frontend
2. **Asincronía**: HTTP es síncrono, MQTT es asíncrono
3. **Broker central**: Es el único que conocen backend y subscriber
4. **Topic como contrato**: Publisher y subscriber acuerdan el topic
5. **No hay respuesta directa**: Subscriber no responde al frontend
6. **Frontend solo recibe confirmación HTTP**, no el print() real