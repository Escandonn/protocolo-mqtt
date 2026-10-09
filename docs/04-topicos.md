# Tópicos MQTT

## Qué es un MQTT Topic

Un **Topic** es una cadena de texto que funciona como **dirección** o **canal** para los mensajes.

Es la forma en que el broker sabe **a quién entregar** cada mensaje.

## Topic Usado en Este Proyecto

```text
demo/mensagem
```

## Estructura Jerárquica

Los topics usan `/` como separador, creando una jerarquía:

```text
demo
└── mensagem
```

Esto permite:
- Suscribirse a `demo/+` (un nivel)
- Suscribirse a `demo/#` (todos los sub-niveles)
- Organizar por dominio: `casa/sala/temperatura`, `casa/cocina/humedad`

## Cómo el Publisher Publica

En `backend/mqtt_client.py`:

```python
TOPIC = "demo/mensagem"

def publish_message(message: str):
    client = mqtt.Client()
    client.connect(BROKER, PORT, 60)
    client.publish(TOPIC, message)  # Publica EN "demo/mensagem"
    client.disconnect()
```

El broker recibe: **topic="demo/mensagem", payload="Hola MQTT"**

## Cómo el Subscriber Se Suscribe

En `mqtt-frontend/subscriber.py`:

```python
TOPIC = "demo/mensagem"

def on_connect(client, userdata, flags, rc):
    client.subscribe(TOPIC)  # Se suscribe A "demo/mensagem"
```

El broker ahora sabe: **este cliente quiere mensajes de "demo/mensagem"**

## Coincidencia Exacta

Para que funcione, **el topic debe ser idéntico**:

| Publisher | Subscriber | ¿Recibe? |
|-----------|------------|----------|
| `demo/mensagem` | `demo/mensagem` | ✅ Sí |
| `demo/mensagem` | `demo/+` | ✅ Sí (wildcard 1 nivel) |
| `demo/mensagem` | `demo/#` | ✅ Sí (wildcard multi-nivel) |
| `demo/mensagem` | `otro/topic` | ❌ No |

## Wildcards (Comodines)

| Wildcard | Significado | Ejemplo |
|----------|-------------|---------|
| `+` | Un nivel exacto | `casa/+/temperatura` coincide con `casa/sala/temperatura` |
| `#` | Cero o más niveles (solo al final) | `casa/#` coincide con todo lo que empiece por `casa/` |

## Mejores Prácticas de Topics

1. **Usa minúsculas**: `demo/mensagem` no `Demo/Mensagem`
2. **Sé descriptivo**: `sensor/temperatura` mejor que `s/t`
3. **Evita empezar con `/`**: `/demo/mensagem` crea topic vacío al inicio
4. **No uses espacios**: `demo/mensagem` no `demo/mensagem`
5. **Jerarquía lógica**: `edificio/planta/habitacion/sensor`

## En Este Proyecto

El topic `demo/mensagem` es simple intencionalmente:
- `demo` = nombre del proyecto/ejemplo
- `mensagem` = tipo de dato que se envía

Esto permite entender el concepto sin complejidad adicional.