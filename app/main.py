"""
Cyber-API — API de Ciberseguridad Defensiva
Curso: Tratamiento de Datos | UIDE-EIG | Feb 2026
Framework: FastAPI + Pydantic
"""

import time
import uuid
import logging
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from app.routes import health, alerts, risk_score
from app.security.auth import unauthorized_handler

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%SZ",
)
logger = logging.getLogger("cyber-api")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("event=startup service=cyber-api version=2.0.0 port=8080")
    yield
    logger.info("event=shutdown service=cyber-api")


# ─── Aplicación ──────────────────────────────────────────────────────────────
app = FastAPI(
    title="Cyber-API",
    description="API de Ciberseguridad Defensiva — UIDE-EIG Tratamiento de Datos Feb 2026",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)


@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())[:8]
    request.state.request_id = request_id
    start = time.time()

    response: Response = await call_next(request)

    elapsed = round((time.time() - start) * 1000, 2)
    client_ip = request.headers.get("x-forwarded-for", request.client.host)
    logger.info(
        f"request_id={request_id} method={request.method} "
        f"path={request.url.path} status={response.status_code} "
        f"time_ms={elapsed} ip={client_ip}"
    )
    response.headers["X-Request-ID"] = request_id
    return response


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    rid = getattr(request.state, "request_id", "unknown")
    logger.error(f"request_id={rid} error=internal_server_error detail={str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"error": "Error interno del servidor", "status": 500},
    )


app.include_router(health.router)
app.include_router(alerts.router)
app.include_router(risk_score.router)
