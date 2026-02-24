Proyecto Tratamiento de Datos
Grupo: 8
Integrantes:
Byron Velasco
Jefferson Ramirez
Edison Cofre
Descripción: Cyber-API — API de Ciberseguridad Defensiva
Descripción

Microservicio REST defensivo en FastAPI. Permite registrar y consultar alertas de seguridad en memoria y calcular un score de riesgo. Incluye validación con Pydantic, autenticación por API Key y documentación automática en /docs.

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

 Prueba de funcionamiento API CLOUD 
 https://github.com/Jefferson0210/Tratamiento_de_Datos_Grupo_8/blob/main/API%20en%20google%20cloud%20.jpg

 Logs funcionamiento API y notificación de errores 
 https://github.com/Jefferson0210/Tratamiento_de_Datos_Grupo_8/blob/main/LOGS%20API%20GCP.jpg
