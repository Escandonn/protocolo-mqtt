# Guía de Ejecución (Windows)

## Requisitos Previos

- Windows 10/11
- Python 3.11+ instalado y en PATH
- Git (opcional)

## Paso a Paso

### 1. Abrir Terminal (PowerShell o CMD)

Presiona `Win + X` → **Terminal (Admin)** o **PowerShell**

### 2. Navegar al Proyecto

```powershell
cd C:\Users\TU_USUARIO\Documents\uni\protoocolo-mqtt
```

### 3. Crear y Activar Entorno Virtual

```powershell
python -m venv venv
venv\Scripts\activate
```

Verás `(venv)` al inicio de la línea de comandos.

### 4. Instalar Dependencias

```powershell
pip install -r requirements.txt
```

Salida esperada:
```text
Successfully installed fastapi-... paho-mqtt-... uvicorn-...
```

### 5. Instalar Mosquitto

**Opción A: Instalador oficial (recomendado)**
1. Ve a https://mosquitto.org/download/
2. Descarga "Windows Native Installer" (última versión)
3. Ejecuta el `.exe` y sigue el asistente
4. **Importante**: Marca "Install as service" si se ofrece

**Opción B: Chocolatey**
```powershell
choco install mosquitto
```

**Opción C: Scoop**
```powershell
scoop install mosquitto
```

### 6. Verificar/Iniciar Mosquitto

**Si se instaló como servicio:**
```powershell
net start mosquitto
```

**Si NO es servicio (ejecutar manual):**
```powershell
mosquitto -v
```
> Mantén esta terminal abierta. Verás logs de conexiones.

### 7. Terminal 1: Ejecutar Mosquitto (si no es servicio)

```powershell
# Terminal 1
mosquitto -v
```

Deja esta terminal corriendo. Verás:
```text
1695734200: mosquitto version 2.0.x starting
1695734200: Using default config.
1695734200: Opening ipv4 listen socket on port 1883.
1695734200: Opening ipv6 listen socket on port 1883.
```

### 8. Terminal 2: Ejecutar Subscriber

Abre **nueva terminal** (Ctrl+Shift+T o nueva pestaña)

```powershell
cd C:\Users\TU_USUARIO\Documents\uni\protoocolo-mqtt
venv\Scripts\activate
python subscriber/subscriber.py
```

Salida esperada:
```text
Conectado al broker MQTT en localhost:1883
Suscrito al topic: demo/mensaje
Esperando mensajes...
```

### 9. Terminal 3: Ejecutar FastAPI

Abre **otra terminal nueva**

```powershell
cd C:\Users\TU_USUARIO\Documents\uni\protoocolo-mqtt
venv\Scripts\activate
uvicorn app.main:app --reload
```

Salida esperada:
```text
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxx] using StatReload
INFO:     Started server process [xxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### 10. Terminal 4: Realizar Petición HTTP

Abre **otra terminal nueva**

```powershell
cd C:\Users\TU_USUARIO\Documents\uni\protoocolo-mqtt
venv\Scripts\activate
curl -X POST http://127.0.0.1:8000/mqtt/publicar -H "Content-Type: application/json" -d "{\"mensaje\":\"Hola MQTT\"}"
```

> **Nota en PowerShell**: Las comillas dobles internas deben escaparse con backslash `\`

**Alternativa con Invoke-WebRequest (PowerShell nativo):**
```powershell
Invoke-WebRequest -Uri "http://127.0.0.1:8000/mqtt/publicar" -Method POST -ContentType "application/json" -Body '{"mensaje":"Hola MQTT"}'
```

## Resultado Esperado

### En Terminal 2 (Subscriber)
```text
Conectado al broker MQTT en localhost:1883
Suscrito al topic: demo/mensaje
Esperando mensajes...

Mensaje recibido: Hola MQTT
```

### En Terminal 4 (Cliente HTTP)
```json
{
  "status": "ok",
  "mensaje": "Hola MQTT"
}
```

### En Terminal 3 (FastAPI)
```text
INFO:     127.0.0.1:xxxxx - "POST /mqtt/publicar HTTP/1.1" 200 OK
Mensaje publicado en demo/mensaje: Hola MQTT
```

### En Terminal 1 (Mosquitto - si usa -v)
```text
1695734205: New connection from 127.0.0.1:xxxxx on port 1883.
1695734205: New client connected from 127.0.0.1 as auto-xxxxx (p2, c1, k60).
1695734205: Sending CONNACK to auto-xxxxx (0, 0)
1695734205: Received PUBLISH from auto-xxxxx (d0, q0, r0, m1, 'demo/mensaje', ... (9 bytes))
1695734205: Sending PUBLISH to auto-yyyyy (d0, q0, r0, m1, 'demo/mensaje', ... (9 bytes))
1695734205: Received DISCONNECT from auto-xxxxx
1695734205: Client auto-xxxxx disconnected.
```

## Resumen de Terminales

| Terminal | Comando | Qué Hace |
|----------|---------|----------|
| 1 | `mosquitto -v` | Broker MQTT (logs visibles) |
| 2 | `python subscriber/subscriber.py` | Escucha e imprime mensajes |
| 3 | `uvicorn app.main:app --reload` | API REST en puerto 8000 |
| 4 | `curl ...` | Envía mensaje de prueba |

## Detener Todo

- **Terminal 1**: `Ctrl+C` (detiene Mosquitto)
- **Terminal 2**: `Ctrl+C` (detiene subscriber)
- **Terminal 3**: `Ctrl+C` (detiene FastAPI)
- **Terminal 4**: No necesario (curl termina solo)

## Solución de Problemas

### "Connection refused" al conectar MQTT
- ¿Mosquitto está corriendo? Verifica Terminal 1
- ¿Puerto 1883 libre? `netstat -an | findstr 1883`

### "Module not found: paho.mqtt"
- ¿Entorno virtual activado? Debe verse `(venv)`
- `pip install paho-mqtt`

### "Address already in use" en FastAPI
- Puerto 8000 ocupado: `netstat -an | findstr 8000`
- Mata proceso o usa `--port 8001`

### curl no funciona en PowerShell
- Usa `Invoke-WebRequest` (ver arriba)
- O instala curl: `winget install curl`
- O usa Git Bash / WSL

## Probar Múltiples Mensajes

En Terminal 4, ejecuta varias veces:
```powershell
curl -X POST http://127.0.0.1:8000/mqtt/publicar -H "Content-Type: application/json" -d "{\"mensaje\":\"Mensaje 1\"}"
curl -X POST http://127.0.0.1:8000/mqtt/publicar -H "Content-Type: application/json" -d "{\"mensaje\":\"Mensaje 2\"}"
curl -X POST http://127.0.0.1:8000/mqtt/publicar -H "Content-Type: application/json" -d "{\"mensaje\":\"Mensaje 3\"}"
```

Verás en Terminal 2:
```text
Mensaje recibido: Mensaje 1
Mensaje recibido: Mensaje 2
Mensaje recibido: Mensaje 3
```

¡Cada mensaje llega independientemente!