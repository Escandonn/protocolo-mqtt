import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883
TOPIC = "demo/mensaje"


def on_connect(client, userdata, flags, rc):
    """Callback cuando se conecta al broker."""
    if rc == 0:
        print(f"Conectado al broker MQTT en {BROKER}:{PORT}")
        client.subscribe(TOPIC)
        print(f"Suscrito al topic: {TOPIC}")
        print("Esperando mensajes...")
    else:
        print(f"Error de conexión: {rc}")


def on_message(client, userdata, msg):
    """Callback cuando llega un mensaje."""
    mensaje = msg.payload.decode()
    print(f"\nMensaje recibido: {mensaje}")


def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    
    try:
        client.connect(BROKER, PORT, 60)
        client.loop_forever()
    except KeyboardInterrupt:
        print("\nDesconectando...")
        client.disconnect()
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()