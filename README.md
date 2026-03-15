Proyecto Tratamiento de Datos;

Grupo: 8; 

Integrantes:;
Byron Velasco;
Jefferson Ramirez;
Edison Cofre;

Descripción: Cyber-API — API de Ciberseguridad Defensiva

## SE MEJORA LA DESCRIPCIÓN DEL ARCHIVO README.md en base a la observación de la semana 1 

La aplicación está construida utilizando **FastAPI** y **Pydantic**, tecnologías modernas de desarrollo de APIs en Python que permiten crear servicios web de alto rendimiento, seguros y fácilmente documentados.

La API está diseñada para centralizar funcionalidades orientadas al análisis y gestión de eventos de seguridad, proporcionando endpoints especializados para monitoreo del estado del sistema (*health*), gestión de alertas de seguridad (*alerts*) y cálculo de niveles de riesgo (*risk_score*). Estos módulos permiten estructurar la lógica de negocio de manera modular y escalable.

El servicio incorpora mecanismos de observabilidad y trazabilidad mediante un middleware de registro que genera identificadores únicos por solicitud (*request_id*), registra el método HTTP, ruta, código de estado, tiempo de respuesta e IP de origen. Esta funcionalidad facilita auditorías, monitoreo operativo y análisis de incidentes de seguridad.

Además, la API implementa un manejador global de excepciones que captura errores inesperados y devuelve respuestas controladas al cliente, evitando la exposición de información sensible del servidor. También se incluyen eventos de ciclo de vida de la aplicación para registrar el inicio y cierre del servicio.

Finalmente, la plataforma expone documentación interactiva automática mediante Swagger y ReDoc, permitiendo a desarrolladores y analistas de seguridad explorar y consumir los endpoints de forma sencilla y eficiente.


Estructura

cyber-api/

app/main.py

app/models/schemas.py

app/routes/health.py

app/routes/alerts.py

app/routes/risk_score.py

app/security/auth.py

Dockerfile

requirements.txt

README.md

Endpoints

GET /health (público)

POST /alerts (protegido con X-API-Key)

GET /alerts (protegido con X-API-Key)

POST /risk-score (protegido con X-API-Key)

GET /docs, /redoc (público)

Uso local

Instalar: pip install -r requirements.txt

Configurar: API_KEY en variables de entorno

Ejecutar: python -m uvicorn app.main:app --host 0.0.0.0 --port 8080

Docker

build: docker build -t cyber-api:v2 .

run: docker run -p 8080:8080 -e API_KEY="tu_clave" cyber-api:v2

Pruebas con curl

GET: curl http://localhost:8080/health

POST alertas: curl -X POST http://localhost:8080/alerts
 -H "Content-Type: application/json" -H "X-API-Key: tu_clave" -d '{...}'

Error sin API key: curl -X POST http://localhost:8080/alerts
 -H "Content-Type: application/json" -d '{...}'

POST risk: curl -X POST http://localhost:8080/risk-score
 -H "Content-Type: application/json" -H "X-API-Key: tu_clave" -d '{...}'

EVIDENCIA DEL PROYECTO 

Validación de contraseñas;

https://github.com/Jefferson0210/Tratamiento_de_Datos_Grupo_8/blob/main/validaci%C3%B3n%20de%20contrase%C3%B1as.jpeg;

API FUNCIONANDO LOCALMENTE;

https://github.com/Jefferson0210/Tratamiento_de_Datos_Grupo_8/blob/main/API%20funcionando%20localmente.jpeg;

CONSTRUCCIÓN DE IMAGEN EN DOCKER;

https://github.com/Jefferson0210/Tratamiento_de_Datos_Grupo_8/blob/main/Docker%202.jpeg;

CONTENEDOR EJECUTANDOSE;

https://github.com/Jefferson0210/Tratamiento_de_Datos_Grupo_8/blob/main/Docker.jpeg;

PRUEBA CURL EXITOSA;

https://github.com/Jefferson0210/Tratamiento_de_Datos_Grupo_8/blob/main/Pruebas%20Curl%201.jpeg;

https://github.com/Jefferson0210/Tratamiento_de_Datos_Grupo_8/blob/main/Pruebas%20Curl%202.jpeg;

API DESPLEGADA EN CLOUD; 

https://github.com/Jefferson0210/Tratamiento_de_Datos_Grupo_8/blob/main/API%20en%20google%20cloud%20.jpg;

https://github.com/Jefferson0210/Tratamiento_de_Datos_Grupo_8/blob/main/API%20FUNCIONANDO%20.jpeg;

https://github.com/Jefferson0210/Tratamiento_de_Datos_Grupo_8/blob/main/LOGS%20API%20GCP.jpg;

ENDPINT ACCESIBLE PUBLICAMENTE;
https://github.com/Jefferson0210/Tratamiento_de_Datos_Grupo_8/blob/main/endpoint%20publico.jpeg

## Respuesta a preguntas planteadas en la Semana 1 
# 1. Como se maneja normalmente en la industria el almacenamiento de API keys de los usuarios?
En la industria, el almacenamiento de API Keys se maneja siguiendo principios similares al manejo de contraseñas: nunca se almacenan en texto plano y se aplican controles de seguridad para evitar filtraciones. A continuación se describen las prácticas más comunes en entornos profesionales
1. Almacenamiento usando hash
2. Separar identificador + secreto
3. Uso de Secret Managers
4. Rotación y expiración de claves
5. Restricciones de seguridad:
Las plataformas suelen aplicar controles adicionales:
Rate limiting
IP allowlist
Scopes o permisos por API
detección de abuso

# Reglas dinámicas basadas en datos

Las recomendaciones pueden generarse mediante motores de reglas que analicen variables del sistema en tiempo real.
Ejemplo:
Nivel de riesgo detectado
Número de alertas recientes
Historial de incidentes
Tipo de activo o sistema afectado



 
