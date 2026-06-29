# Cyber-API

![Python](https://img.shields.io/badge/Python-3.11-3776AB)
![FastAPI](https://img.shields.io/badge/FastAPI-009688)
![Docker](https://img.shields.io/badge/Docker-2496ED)
![Google Cloud](https://img.shields.io/badge/Google%20Cloud-deployed-4285F4)

**API de ciberseguridad defensiva para centralizar el análisis y la gestión de eventos de seguridad.**

Cuando algo raro pasa en un sistema, la pregunta no es solo *"¿qué pasó?"*, sino *"¿qué tan grave es y qué hago ahora?"*. Cyber-API responde justo eso: recibe alertas de seguridad, calcula un nivel de riesgo y deja todo registrado y auditable, a través de una API rápida, documentada y lista para producción. Construida con FastAPI y Pydantic, contenerizada con Docker y desplegada en Google Cloud.

---

## Qué hace

Cyber-API centraliza la lógica de seguridad en endpoints especializados y modulares:

- **Monitoreo del sistema** (`health`) — comprobar al instante que el servicio está vivo y respondiendo.
- **Gestión de alertas** (`alerts`) — registrar y consultar eventos de seguridad.
- **Cálculo de riesgo** (`risk-score`) — convertir los datos de un evento en un nivel de riesgo accionable.

Cada módulo está separado para que la lógica de negocio sea clara, escalable y fácil de mantener.

---

## Lo que la hace seria

- **Trazabilidad por solicitud** — un middleware genera un `request_id` único por petición y registra método HTTP, ruta, código de estado, tiempo de respuesta e IP de origen. Esto convierte cada llamada en algo auditable: clave para investigar incidentes.
- **Manejo global de errores** — un manejador central captura los errores inesperados y devuelve respuestas controladas, sin filtrar información interna del servidor al cliente.
- **Eventos de ciclo de vida** — la aplicación registra su arranque y su cierre, útil para monitoreo operativo.
- **Autenticación por API Key** — los endpoints sensibles exigen una cabecera `X-API-Key`; lo público y lo protegido están claramente separados.
- **Documentación automática** — Swagger y ReDoc listos para que cualquier desarrollador o analista explore y pruebe los endpoints.

---

## Stack

FastAPI · Pydantic · Python · Docker · Google Cloud

---

## Endpoints

| Método | Ruta | Acceso |
|--------|------|--------|
| `GET` | `/health` | Público |
| `POST` | `/alerts` | Protegido (`X-API-Key`) |
| `GET` | `/alerts` | Protegido (`X-API-Key`) |
| `POST` | `/risk-score` | Protegido (`X-API-Key`) |
| `GET` | `/docs`, `/redoc` | Público |

---

## Cómo usarla

### En local

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Configurar la clave (variable de entorno)
export API_KEY="tu_clave"          # en Windows: set API_KEY=tu_clave

# 3. Ejecutar
python -m uvicorn app.main:app --host 0.0.0.0 --port 8080
```

Documentación interactiva en `http://localhost:8080/docs`.

### Con Docker

```bash
# Construir la imagen
docker build -t cyber-api:v2 .

# Ejecutar el contenedor
docker run -p 8080:8080 -e API_KEY="tu_clave" cyber-api:v2
```

### Probar con curl

```bash
# Health (público)
curl http://localhost:8080/health

# Crear alerta (protegido)
curl -X POST http://localhost:8080/alerts \
  -H "Content-Type: application/json" \
  -H "X-API-Key: tu_clave" \
  -d '{ ... }'

# Calcular riesgo (protegido)
curl -X POST http://localhost:8080/risk-score \
  -H "Content-Type: application/json" \
  -H "X-API-Key: tu_clave" \
  -d '{ ... }'
```

Si llamas a un endpoint protegido sin la cabecera `X-API-Key`, la API responde con un error controlado (acceso denegado).

---

## Estructura del proyecto

```
cyber-api/
├── app/
│   ├── main.py                 # App, middleware de logging, manejo de errores
│   ├── models/schemas.py       # Modelos Pydantic (validación de entradas/salidas)
│   ├── routes/
│   │   ├── health.py           # Estado del servicio
│   │   ├── alerts.py           # Gestión de alertas
│   │   └── risk_score.py       # Cálculo de nivel de riesgo
│   └── security/auth.py        # Autenticación por API Key
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## Buenas prácticas y roadmap

El proyecto aplica criterio de seguridad desde el diseño. Algunas prácticas ya están implementadas y otras marcan la dirección a futuro:

**Almacenamiento seguro de API Keys.** Igual que con las contraseñas, las claves nunca deberían guardarse en texto plano. El enfoque profesional contempla:
- Guardar solo el **hash** de la clave, no la clave en sí.
- Separar **identificador + secreto**.
- Usar **Secret Managers** en vez de hardcodear claves.
- **Rotación y expiración** periódica de claves.
- Controles extra: **rate limiting**, **IP allowlist**, **scopes** por API y **detección de abuso**.

**Reglas de riesgo dinámicas.** El cálculo de riesgo puede crecer hacia un motor de reglas que analice variables en tiempo real: nivel de riesgo detectado, número de alertas recientes, historial de incidentes y tipo de activo afectado.

---



## Objetivo

Diseñar, construir y desplegar una API funcional aplicando buenas prácticas de desarrollo: versionamiento, pruebas, contenerización y despliegue (local, Docker y nube) con FastAPI.

 
