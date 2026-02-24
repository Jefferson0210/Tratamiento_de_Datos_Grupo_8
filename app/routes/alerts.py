import uuid
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, Request, Query
from fastapi.responses import JSONResponse

from app.models.schemas import AlertaEntrada, AlertaSalida, AlertaLista
from app.security.auth import verify_api_key

router = APIRouter(tags=["Alertas"])

alerts_store: list[dict] = []


@router.post(
    "/alerts",
    status_code=201,
    response_model=dict,
    summary="Registrar alerta de seguridad",
    dependencies=[Depends(verify_api_key)],
)
async def crear_alerta(alerta: AlertaEntrada, request: Request):
    """
    Recibe un evento de seguridad validado y lo guarda en memoria.

    - **tipo**: login_fallido | escaneo_puertos | ddos | malware | phishing | otro
    - **severidad**: baja | media | alta | critica
    - **ip_origen**: IP de origen del evento
    - **usuario**: usuario involucrado
    - **mensaje**: descripción del evento (5–500 caracteres)
    """
    rid = getattr(request.state, "request_id", "n/a")

    nueva = {
        "id":         str(uuid.uuid4()),
        "tipo":       alerta.tipo.value,
        "severidad":  alerta.severidad.value,
        "ip_origen":  alerta.ip_origen,
        "usuario":    alerta.usuario,
        "mensaje":    alerta.mensaje,
        "timestamp":  datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "request_id": rid,
    }
    alerts_store.append(nueva)

    return JSONResponse(
        status_code=201,
        content={
            "mensaje": "Alerta registrada exitosamente",
            "alerta":  nueva,
        },
    )


@router.get(
    "/alerts",
    response_model=AlertaLista,
    summary="Listar alertas registradas",
    dependencies=[Depends(verify_api_key)],
)
async def listar_alertas(
    page:      int            = Query(default=1,    ge=1,   description="Número de página"),
    limit:     int            = Query(default=10,   ge=1,   le=100, description="Resultados por página"),
    severidad: Optional[str]  = Query(default=None, description="Filtrar por severidad: baja|media|alta|critica"),
):
    """
    Lista todas las alertas en memoria.
    Soporta paginación (`page`, `limit`) y filtro por `severidad`.
    """
    datos = alerts_store

    if severidad:
        datos = [a for a in datos if a["severidad"] == severidad.lower()]

    total  = len(datos)
    inicio = (page - 1) * limit
    fin    = inicio + limit

    return {
        "total":   total,
        "pagina":  page,
        "limit":   limit,
        "alertas": datos[inicio:fin],
    }
