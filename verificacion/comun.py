"""Utilidades de las verificaciones deterministas: correr un comando y esperar a que una URL responda."""
import subprocess
import time
from pathlib import Path

import httpx

RAIZ = Path(__file__).resolve().parent.parent
APP = RAIZ / "app"
SALIDA = RAIZ / "salida"


def responde(url: str, intentos: int = 30) -> tuple[bool, str]:
    for _ in range(intentos):
        try:
            r = httpx.get(url, timeout=2)
            if r.status_code < 400:
                return True, f"{url} -> {r.status_code}"
        except httpx.HTTPError:
            pass
        time.sleep(1)
    return False, f"{url} no respondió en {intentos} s"


def correr(comando: list[str], cwd: Path, timeout: int = 600) -> tuple[bool, str]:
    r = subprocess.run(comando, cwd=cwd, capture_output=True, text=True,
                       encoding="utf-8", errors="replace", timeout=timeout)
    return r.returncode == 0, ((r.stdout or "") + (r.stderr or ""))[-4000:]
