from fastapi import FastAPI
from pydantic import BaseModel
from app.mqtt_client import publish_message

app = FastAPI(title="FastAPI MQTT Demo")


class MensajeRequest(BaseModel):
    mensaje: str


@app.post("/mqtt/publicar")
async def publicar_mensaje(request: MensajeRequest):
    """
    Endpoint que recibe un mensaje por HTTP y lo publica vía MQTT.
    
    Flujo:
    1. Recibe JSON con campo "mensaje"
    2. Publica el mensaje en el topic MQTT "demo/mensaje"
    3. Retorna confirmación
    """
    exito = publish_message(request.mensaje)
    
    return {
        "status": "ok" if exito else "error",
        "mensaje": request.mensaje
    }


@app.get("/")
async def root():
    return {"message": "FastAPI MQTT Demo - Usa POST /mqtt/publicar"}