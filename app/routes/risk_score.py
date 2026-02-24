
from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse

from app.models.schemas import RiskInput, RiskOutput
from app.security.auth import verify_api_key

router = APIRouter(tags=["Risk Score"])


# ─── Tablas de recomendaciones ────────────────────────────────────────────────
NIVELES = {
    "bajo":    (0,  29),
    "medio":   (30, 59),
    "alto":    (60, 79),
    "critico": (80, 100),
}

RECOMENDACIONES = {
    "bajo":    "Monitoreo rutinario. Sin acción inmediata requerida.",
    "medio":   "Revisar logs, verificar identidad del usuario e IP origen.",
    "alto":    "Bloquear IP temporalmente, notificar al equipo de seguridad.",
    "critico": "Acción inmediata: aislar recurso, iniciar respuesta a incidentes.",
}


def calcular_nivel(score: int) -> str:
    for nivel, (low, high) in NIVELES.items():
        if low <= score <= high:
            return nivel
    return "critico"


# ─── POST /risk-score ─────────────────────────────────────────────────────────
@router.post(
    "/risk-score",
    response_model=RiskOutput,
    summary="Calcular score de riesgo (0–100)",
    dependencies=[Depends(verify_api_key)],
)
async def risk_score(metricas: RiskInput, request: Request):
    """
    Calcula un **Risk Score ponderado** (0–100) a partir de métricas de amenaza:

    | Campo              | Peso | Descripción                              |
    |--------------------|------|------------------------------------------|
    | intentos_fallidos  | 30%  | Intentos de autenticación fallidos (0–50)|
    | ip_reputacion      | 25%  | Reputación IP: 0=limpia, 10=maliciosa    |
    | severidad_num      | 30%  | Severidad del evento: 0=nula, 10=crítica |
    | numero_alertas     | 15%  | Alertas previas del mismo origen (0–100) |

    Devuelve: `score`, `nivel` (bajo/medio/alto/critico) y `recomendacion`.
    """
    score = round(
        (metricas.intentos_fallidos / 50)  * 30 +
        (metricas.ip_reputacion     / 10)  * 25 +
        (metricas.severidad_num     / 10)  * 30 +
        (metricas.numero_alertas    / 100) * 15
    )

    nivel = calcular_nivel(score)

    return {
        "score":         score,
        "nivel":         nivel,
        "recomendacion": RECOMENDACIONES[nivel],
        "inputs":        metricas,
    }
