
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from datetime import datetime, timezone

from app.security.auth import API_KEY  

router = APIRouter(tags=["Health"])

import app.routes.alerts as _alerts_module


@router.get(
    "/health",
    summary="Estado del servicio",
    response_description="Servicio operativo",
)
async def health():
    """
    Endpoint público. Devuelve el estado actual del servicio,
    la versión y la cantidad de alertas en memoria.
    """
    return JSONResponse(
        status_code=200,
        content={
            "status":              "ok",
            "servicio":            "cyber-api",
            "version":             "2.0.0",
            "timestamp":           datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "alertas_en_memoria":  len(_alerts_module.alerts_store),
            "autenticacion":       "X-API-Key requerida en /alerts y /risk-score",
            "docs":                "/docs",
        },
    )
