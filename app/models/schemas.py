from pydantic import BaseModel, Field, field_validator
from typing import Literal, Optional
from datetime import datetime
from enum import Enum


class Severidad(str, Enum):
    baja    = "baja"
    media   = "media"
    alta    = "alta"
    critica = "critica"


class TipoEvento(str, Enum):
    login_fallido   = "login_fallido"
    escaneo_puertos = "escaneo_puertos"
    ddos            = "ddos"
    malware         = "malware"
    phishing        = "phishing"
    otro            = "otro"


class AlertaEntrada(BaseModel):
    tipo:       TipoEvento = Field(..., description="Tipo de evento de seguridad")
    severidad:  Severidad  = Field(..., description="Nivel de severidad del evento")
    ip_origen:  str        = Field(..., min_length=7, max_length=45, description="IP de origen del evento")
    usuario:    str        = Field(..., min_length=1, max_length=100, description="Usuario involucrado")
    mensaje:    str        = Field(..., min_length=5, max_length=500, description="Descripción del evento")

    model_config = {
        "json_schema_extra": {
            "example": {
                "tipo":      "login_fallido",
                "severidad": "alta",
                "ip_origen": "192.168.1.55",
                "usuario":   "admin",
                "mensaje":   "5 intentos fallidos consecutivos detectados"
            }
        }
    }


class AlertaSalida(AlertaEntrada):
    id:         str
    timestamp:  str
    request_id: str


class AlertaLista(BaseModel):
    total:   int
    pagina:  int
    limit:   int
    alertas: list[AlertaSalida]


class RiskInput(BaseModel):
    intentos_fallidos: int = Field(..., ge=0, le=50,  description="Intentos de login fallidos (0–50)")
    ip_reputacion:     int = Field(..., ge=0, le=10,  description="Reputación de IP: 0=confiable, 10=maliciosa")
    severidad_num:     int = Field(..., ge=0, le=10,  description="Severidad numérica: 0=nula, 10=crítica")
    numero_alertas:    int = Field(..., ge=0, le=100, description="Alertas previas del mismo origen (0–100)")

    model_config = {
        "json_schema_extra": {
            "example": {
                "intentos_fallidos": 35,
                "ip_reputacion":     8,
                "severidad_num":     7,
                "numero_alertas":   60
            }
        }
    }


class RiskOutput(BaseModel):
    score:         int   = Field(..., ge=0, le=100)
    nivel:         str
    recomendacion: str
    inputs:        RiskInput
