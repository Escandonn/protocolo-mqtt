from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from mqtt_client import publish_message
from datetime import datetime

app = FastAPI(title="FastAPI MQTT Demo")

# Permitir CORS para que el frontend (Astro) pueda hacer fetch
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class MensagemRequest(BaseModel):
    mensagem: str


@app.post("/mqtt/publicar")
async def publicar_mensagem(request: MensagemRequest):
    """
    Endpoint que recibe un mensaje por HTTP y lo publica vía MQTT.
    
    Flujo:
    1. Recibe JSON con campo "mensagem"
    2. Publica el mensaje en el topic MQTT "demo/mensagem"
    3. Retorna confirmación con timestamp
    """
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
            "documentacion": "/docs"
        }
    }