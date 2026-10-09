import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883
TOPIC = "demo/mensaje"


def publish_message(message: str) -> bool:
    """
    Conecta al broker MQTT y publica un mensaje en el topic configurado.
    
    Args:
        message: El mensaje a publicar
        
    Returns:
        True si se publicó correctamente, False en caso contrario
    """
    client = mqtt.Client()
    
    try:
        client.connect(BROKER, PORT, 60)
        result = client.publish(TOPIC, message)
        client.disconnect()
        
        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            print(f"Mensaje publicado en {TOPIC}: {message}")
            return True
        else:
            print(f"Error al publicar: {result.rc}")
            return False
            
    except Exception as e:
        print(f"Error de conexión MQTT: {e}")
        return False