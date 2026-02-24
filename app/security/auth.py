
import os
from fastapi import Security, HTTPException, Request
from fastapi.security.api_key import APIKeyHeader

API_KEY       = os.environ.get("API_KEY", "clave-secreta-demo-2026")
API_KEY_NAME  = "X-API-Key"

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def verify_api_key(api_key: str = Security(api_key_header)) -> str:
    if not api_key or api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail={
                "error":   "No autorizado",
                "detalle": "Header X-API-Key ausente o incorrecto",
                "status":  401,
            },
        )
    return api_key

def unauthorized_handler():
    return {
        "error":   "No autorizado",
        "detalle": "Header X-API-Key ausente o incorrecto",
        "status":  401,
    }
