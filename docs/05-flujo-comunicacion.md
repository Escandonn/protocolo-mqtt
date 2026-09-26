# Flujo de Comunicación

## Flujo Completo

```text
Cliente
   │
   │ HTTP POST /mqtt/publicar {"mensaje": "Hola"}
   ▼
FastAPI
   │
   │ publish_message("Hola")
   ▼
MQTT Broker
   │
   │ mensaje "Hola" en topic "demo/mensaje"
   ▼
Python Subscriber
   │
   │ callback on_message()
   ▼
print("Mensaje recibido: Hola")
```

## Explicación Paso a Paso

### Paso 1: Cliente → FastAPI (HTTP)

**Qué ocurre:**
- Usuario ejecuta `curl` o usa Postman
- Se envía petición POST a `http://127.0.0.1:8000/mqtt/publicar`
- Headers: `Content-Type: application/json`
- Body: `{"mensaje": "Hola MQTT"}`

**Protocolo:** HTTP/1.1 (Request/Response)
**Puerto:** 8000 (FastAPI/Uvicorn)

---

### Paso 2: FastAPI Valida y Procesa

**Qué ocurre en `app/main.py`:**
1. FastAPI recibe la petición
2. Pydantic valida el JSON contra `MensajeRequest`
3. Si es válido, extrae `request.mensaje`
4. Llama a `publish_message(request.mensaje)`

**Código:**
```python
@app.post("/mqtt/publicar")
async def publicar_mensaje(request: MensajeRequest):
    exito = publish_message(request.mensaje)
    return {"status": "ok" if exito else "error", "mensaje": request.mensaje}
```

**Importante:** FastAPI **no espera** al subscriber. Retorna inmediato.

---

### Paso 3: FastAPI → MQTT Broker (Publish)

**Qué ocurre en `app/mqtt_client.py`:**
1. Crea cliente MQTT nuevo
2. Conecta a `localhost:1883`
3. Ejecuta `client.publish("demo/mensaje", "Hola MQTT")`
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
1. Recibe paquete PUBLISH en topic `demo/mensaje`
2. Busca en su tabla de suscripciones
3. Encuentra a `subscriber.py` suscrito a `demo/mensaje`
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

**Qué ocurre en `subscriber/subscriber.py`:**
1. Se ejecuta `on_message(client, userdata, msg)`
2. `msg.payload` contiene los bytes del mensaje
3. Decodifica: `msg.payload.decode()` → `"Hola MQTT"`
4. Ejecuta `print(f"Mensaje recibido: {mensaje}")`

**Código:**
```python
def on_message(client, userdata, msg):
    mensaje = msg.payload.decode()
    print(f"\nMensaje recibido: {mensaje}")
```

---

### Paso 7: Resultado Visible

En la terminal donde corre `subscriber.py`:
```text
Mensaje recibido: Hola MQTT
```

En la terminal del cliente (curl):
```json
{
  "status": "ok",
  "mensaje": "Hola MQTT"
}
```

## Resumen de Protocolos y Puertos

| Tramo | Protocolo | Puerto | Dirección |
|-------|-----------|--------|-----------|
| Cliente → FastAPI | HTTP | 8000 | Request/Response |
| FastAPI → Broker | MQTT | 1883 | Publish |
| Broker → Subscriber | MQTT | 1883 | Push (async) |

## Puntos Clave para Entender

1. **Desacoplamiento**: FastAPI no conoce a subscriber.py
2. **Asincronía**: HTTP es síncrono, MQTT es asíncrono
3. **Broker central**: Es el único que conocen ambos lados
4. **Topic como contrato**: Publisher y subscriber acuerdan el topic
5. **No hay respuesta directa**: Subscriber no responde a FastAPI