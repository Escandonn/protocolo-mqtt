# Tópicos MQTT

## Qué es un MQTT Topic

Un **Topic** es una cadena de texto que funciona como **dirección** o **canal** para los mensajes.

Es la forma en que el broker sabe **a quién entregar** cada mensaje.

## Topic Usado en Este Proyecto

```text
demo/mensaje
```

## Estructura Jerárquica

Los topics usan `/` como separador, creando una jerarquía:

```text
demo
└── mensaje
```

Esto permite:
- Suscribirse a `demo/+` (un nivel)
- Suscribirse a `demo/#` (todos los sub-niveles)
- Organizar por dominio: `casa/sala/temperatura`, `casa/cocina/humedad`

## Cómo el Publisher Publica

En `app/mqtt_client.py`:

```python
TOPIC = "demo/mensaje"

def publish_message(message: str):
    client = mqtt.Client()
    client.connect(BROKER, PORT, 60)
    client.publish(TOPIC, message)  # Publica EN "demo/mensaje"
    client.disconnect()
```

El broker recibe: **topic="demo/mensaje", payload="Hola MQTT"**

## Cómo el Subscriber Se Suscribe

En `subscriber/subscriber.py`:

```python
TOPIC = "demo/mensaje"

def on_connect(client, userdata, flags, rc):
    client.subscribe(TOPIC)  # Se suscribe A "demo/mensaje"
```

El broker ahora sabe: **este cliente quiere mensajes de "demo/mensaje"**

## Coincidencia Exacta

Para que funcione, **el topic debe ser idéntico**:

| Publisher | Subscriber | ¿Recibe? |
|-----------|------------|----------|
| `demo/mensaje` | `demo/mensaje` | ✅ Sí |
| `demo/mensaje` | `demo/+` | ✅ Sí (wildcard 1 nivel) |
| `demo/mensaje` | `demo/#` | ✅ Sí (wildcard multi-nivel) |
| `demo/mensaje` | `otro/topic` | ❌ No |

## Wildcards (Comodines)

| Wildcard | Significado | Ejemplo |
|----------|-------------|---------|
| `+` | Un nivel exacto | `casa/+/temperatura` coincide con `casa/sala/temperatura` |
| `#` | Cero o más niveles (solo al final) | `casa/#` coincide con todo lo que empiece por `casa/` |

## Mejores Prácticas de Topics

1. **Usa minúsculas**: `demo/mensaje` no `Demo/Mensaje`
2. **Sé descriptivo**: `sensor/temperatura` mejor que `s/t`
3. **Evita empezar con `/`**: `/demo/mensaje` crea topic vacío al inicio
4. **No uses espacios**: `demo/mensaje` no `demo/mensaje`
5. **Jerarquía lógica**: `edificio/planta/habitacion/sensor`

## En Este Proyecto

El topic `demo/mensaje` es simple intencionalmente:
- `demo` = nombre del proyecto/ejemplo
- `mensaje` = tipo de dato que se envía

Esto permite entender el concepto sin complejidad adicional.