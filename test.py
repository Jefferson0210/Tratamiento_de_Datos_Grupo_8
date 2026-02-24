"""
test.py — Pruebas de integración para Cyber-API
Equivalente Python de los comandos curl del README.
Uso: python test.py
Requiere el servidor corriendo en http://localhost:8080
"""

import requests
import json

BASE    = "http://localhost:8080"
API_KEY = "clave-secreta-demo-2026"
HAUTH   = {"X-API-Key": API_KEY, "Content-Type": "application/json"}
HNOAUTH = {"Content-Type": "application/json"}

# ─── helpers de salida ────────────────────────────────────────────────────────
V = "\033[92m"; R = "\033[91m"; A = "\033[94m"; B = "\033[1m"; X = "\033[0m"


def sep(titulo):
    print(f"\n{A}{B}{'─'*55}{X}\n{A}{B}  {titulo}{X}\n{A}{B}{'─'*55}{X}")


def show(res):
    ok  = res.status_code < 400
    sym = f"{V}✓" if ok else f"{R}✗"
    print(f"{sym} HTTP {res.status_code}{X}")
    try:
        print(json.dumps(res.json(), indent=2, ensure_ascii=False))
    except Exception:
        print(res.text)


# ── 1. GET /health ─────────────────────────────────────────────────────────────
sep("TEST 1 — GET /health  (público, sin key)")
show(requests.get(f"{BASE}/health"))

# ── 2. POST /alerts — alerta válida ───────────────────────────────────────────
sep("TEST 2 — POST /alerts  (201 esperado)")
show(requests.post(f"{BASE}/alerts", json={
    "tipo":      "login_fallido",
    "severidad": "alta",
    "ip_origen": "192.168.1.55",
    "usuario":   "admin",
    "mensaje":   "5 intentos fallidos consecutivos detectados"
}, headers=HAUTH))

# ── 3. POST /alerts — segunda alerta ──────────────────────────────────────────
sep("TEST 3 — POST /alerts  segunda alerta (malware)")
show(requests.post(f"{BASE}/alerts", json={
    "tipo":      "malware",
    "severidad": "critica",
    "ip_origen": "10.0.0.99",
    "usuario":   "servicio-backend",
    "mensaje":   "Proceso sospechoso detectado intentando exfiltrar datos"
}, headers=HAUTH))

# ── 4. POST /alerts SIN API Key → 401 ─────────────────────────────────────────
sep("TEST 4 — POST /alerts  SIN X-API-Key  → 401 esperado")
show(requests.post(f"{BASE}/alerts", json={
    "tipo": "ddos", "severidad": "alta",
    "ip_origen": "1.2.3.4", "usuario": "anon", "mensaje": "flood detectado"
}, headers=HNOAUTH))

# ── 5. POST /alerts — campo faltante → 422 ────────────────────────────────────
sep("TEST 5 — POST /alerts  campo faltante  → 422 esperado")
show(requests.post(f"{BASE}/alerts", json={
    "tipo": "phishing", "severidad": "media"
}, headers=HAUTH))

# ── 6. POST /alerts — severidad inválida → 422 ────────────────────────────────
sep("TEST 6 — POST /alerts  severidad inválida  → 422 esperado")
show(requests.post(f"{BASE}/alerts", json={
    "tipo":      "phishing",
    "severidad": "ultra-mega",      # no existe
    "ip_origen": "10.0.0.1",
    "usuario":   "user1",
    "mensaje":   "Email de phishing detectado"
}, headers=HAUTH))

# ── 7. GET /alerts — listar ────────────────────────────────────────────────────
sep("TEST 7 — GET /alerts  (paginación page=1&limit=5)")
show(requests.get(f"{BASE}/alerts?page=1&limit=5", headers=HAUTH))

# ── 8. GET /alerts — filtro por severidad ─────────────────────────────────────
sep("TEST 8 — GET /alerts?severidad=alta")
show(requests.get(f"{BASE}/alerts?severidad=alta", headers=HAUTH))

# ── 9. POST /risk-score — riesgo alto ─────────────────────────────────────────
sep("TEST 9 — POST /risk-score  (nivel alto esperado)")
show(requests.post(f"{BASE}/risk-score", json={
    "intentos_fallidos": 35,
    "ip_reputacion":      8,
    "severidad_num":      7,
    "numero_alertas":    60
}, headers=HAUTH))

# ── 10. POST /risk-score — riesgo bajo ────────────────────────────────────────
sep("TEST 10 — POST /risk-score  (nivel bajo esperado)")
show(requests.post(f"{BASE}/risk-score", json={
    "intentos_fallidos": 2,
    "ip_reputacion":     1,
    "severidad_num":     1,
    "numero_alertas":    3
}, headers=HAUTH))

# ── 11. POST /risk-score SIN API Key → 401 ────────────────────────────────────
sep("TEST 11 — POST /risk-score  SIN X-API-Key  → 401 esperado")
show(requests.post(f"{BASE}/risk-score", json={
    "intentos_fallidos": 10, "ip_reputacion": 5,
    "severidad_num": 4, "numero_alertas": 20
}, headers=HNOAUTH))

# ── 12. Endpoint inexistente → 404 ────────────────────────────────────────────
sep("TEST 12 — GET /no-existe  → 404 esperado")
show(requests.get(f"{BASE}/no-existe"))

print(f"\n{V}{B}✓ Todas las pruebas completadas.{X}\n")
