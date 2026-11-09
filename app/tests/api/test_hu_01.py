"""Pruebas de API para HU-01: Registro de empleados."""
import re
import uuid

import httpx
import pytest


# ---------------------------------------------------------------------------
# CP-01: Registro exitoso de un empleado nuevo
# ---------------------------------------------------------------------------

def test_cp01_registro_exitoso(url_api):
    """CP-01: Registro exitoso de un empleado nuevo via API.

    Envía un POST con datos válidos y verifica que la respuesta sea 201,
    incluya numero_empleado en formato EMP-NNNN, estado 'activo' y correo
    en minúsculas.
    """
    correo_unico = f"ana.lopez.{uuid.uuid4().hex[:8]}@empresa.com"
    payload = {
        "nombre": "Ana López",
        "correo": correo_unico,
        "puesto": "Analista de Datos",
        "departamento": "Tecnología",
        "fecha_ingreso": "2026-11-08",
    }

    response = httpx.post(f"{url_api}/api/empleados", json=payload)

    assert response.status_code == 201, (
        f"Se esperaba 201, se obtuvo {response.status_code}. "
        f"Cuerpo: {response.text}"
    )

    cuerpo = response.json()

    assert "numero_empleado" in cuerpo, (
        "La respuesta no contiene el campo 'numero_empleado'."
    )
    assert re.match(r"EMP-\d{4}", cuerpo["numero_empleado"]), (
        f"El campo numero_empleado '{cuerpo['numero_empleado']}' "
        "no tiene el formato EMP-NNNN."
    )

    assert cuerpo.get("estado") == "activo", (
        f"Se esperaba estado='activo', se obtuvo '{cuerpo.get('estado')}'."
    )

    assert cuerpo.get("correo") == correo_unico.lower(), (
        f"El correo en la respuesta '{cuerpo.get('correo')}' "
        f"no coincide con '{correo_unico.lower()}'."
    )


# ---------------------------------------------------------------------------
# CP-03: Rechazo por correo duplicado sin importar mayúsculas
# ---------------------------------------------------------------------------

def test_cp03_rechazo_correo_duplicado(url_api):
    """CP-03: Rechazo por correo duplicado sin importar mayúsculas.

    Registra primero un empleado y luego intenta registrar otro con el mismo
    correo en mayúsculas. La API debe responder 409 con el mensaje esperado.
    """
    correo_base = f"pedro.garcia.{uuid.uuid4().hex[:8]}@empresa.com"
    payload_original = {
        "nombre": "Pedro García",
        "correo": correo_base,
        "puesto": "Ejecutivo de Ventas",
        "departamento": "Ventas",
        "fecha_ingreso": "2026-11-08",
    }
    # Crear el empleado original
    r_crear = httpx.post(f"{url_api}/api/empleados", json=payload_original)
    assert r_crear.status_code == 201, (
        f"Fallo al crear el empleado de precondición: {r_crear.text}"
    )

    # Intentar duplicar con el correo en mayúsculas
    payload_duplicado = {
        "nombre": "Pedro García",
        "correo": correo_base.upper(),
        "puesto": "Ejecutivo de Ventas",
        "departamento": "Ventas",
        "fecha_ingreso": "2026-11-08",
    }
    response = httpx.post(f"{url_api}/api/empleados", json=payload_duplicado)

    assert response.status_code == 409, (
        f"Se esperaba 409, se obtuvo {response.status_code}. "
        f"Cuerpo: {response.text}"
    )

    cuerpo = response.json()
    assert cuerpo.get("detail") == "El correo ya está registrado", (
        f"Mensaje inesperado: '{cuerpo.get('detail')}'."
    )


# ---------------------------------------------------------------------------
# CP-04: Rechazo por correo con dominio no corporativo
# ---------------------------------------------------------------------------

def test_cp04_rechazo_dominio_no_corporativo(url_api):
    """CP-04: Rechazo por correo con dominio no corporativo.

    Envía un POST con un correo de dominio externo (@gmail.com) y verifica
    que la API responda 422 con el mensaje de dominio corporativo.
    """
    payload = {
        "nombre": "María Ruiz",
        "correo": f"maria.ruiz.{uuid.uuid4().hex[:8]}@gmail.com",
        "puesto": "Contadora",
        "departamento": "Finanzas",
        "fecha_ingreso": "2026-11-08",
    }

    response = httpx.post(f"{url_api}/api/empleados", json=payload)

    assert response.status_code == 422, (
        f"Se esperaba 422, se obtuvo {response.status_code}. "
        f"Cuerpo: {response.text}"
    )

    cuerpo = response.json()
    assert cuerpo.get("detail") == "Usa el correo corporativo @empresa.com", (
        f"Mensaje inesperado: '{cuerpo.get('detail')}'."
    )


# ---------------------------------------------------------------------------
# CP-05: Rechazo por campo obligatorio ausente
# ---------------------------------------------------------------------------

def test_cp05_rechazo_campo_obligatorio_ausente(url_api):
    """CP-05: Rechazo por campo obligatorio ausente (puesto).

    Envía un POST sin el campo 'puesto' y verifica que la API responda 422
    con una referencia explícita al campo faltante.
    """
    payload = {
        "nombre": "Luis Torres",
        "correo": f"luis.torres.{uuid.uuid4().hex[:8]}@empresa.com",
        "departamento": "Operaciones",
        "fecha_ingreso": "2026-11-08",
        # campo 'puesto' ausente intencionalmente
    }

    response = httpx.post(f"{url_api}/api/empleados", json=payload)

    assert response.status_code == 422, (
        f"Se esperaba 422, se obtuvo {response.status_code}. "
        f"Cuerpo: {response.text}"
    )

    respuesta_texto = response.text.lower()
    assert "puesto" in respuesta_texto, (
        f"El cuerpo de la respuesta no referencia el campo 'puesto'. "
        f"Cuerpo: {response.text}"
    )


# ---------------------------------------------------------------------------
# CP-06: Rechazo por fecha de ingreso futura
# ---------------------------------------------------------------------------

def test_cp06_rechazo_fecha_futura(url_api):
    """CP-06: Rechazo por fecha de ingreso futura.

    Envía un POST con una fecha de ingreso en el futuro (2027-01-01) y
    verifica que la API responda 422 con el mensaje correspondiente.
    """
    payload = {
        "nombre": "Carla Nuñez",
        "correo": f"carla.nunez.{uuid.uuid4().hex[:8]}@empresa.com",
        "puesto": "Gerente de Operaciones",
        "departamento": "Operaciones",
        "fecha_ingreso": "2027-01-01",
    }

    response = httpx.post(f"{url_api}/api/empleados", json=payload)

    assert response.status_code == 422, (
        f"Se esperaba 422, se obtuvo {response.status_code}. "
        f"Cuerpo: {response.text}"
    )

    cuerpo = response.json()
    assert cuerpo.get("detail") == "La fecha de ingreso no puede ser futura", (
        f"Mensaje inesperado: '{cuerpo.get('detail')}'."
    )
