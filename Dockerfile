
FROM python:3.14-slim

LABEL maintainer="Jefferson — UIDE-EIG Tratamiento de Datos Feb 2026"
LABEL description="Cyber-API: API de Ciberseguridad Defensiva"
LABEL version="2.0.0"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ENV PORT=8080

ENV API_KEY=clave-secreta-demo-2026

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "1"]
