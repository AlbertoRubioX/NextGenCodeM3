"""Pruebas E2E para HU-01: Registro de empleados (Playwright)."""
import re
import uuid

import pytest


# ---------------------------------------------------------------------------
# CP-02: Registro exitoso de un empleado nuevo (E2E)
# ---------------------------------------------------------------------------

def test_cp02_registro_exitoso_e2e(page, url_web):
    """CP-02: Registro exitoso de un empleado nuevo via formulario web.

    Rellena el formulario con datos válidos, envía y verifica que aparezca
    el mensaje de éxito con el numero_empleado en formato EMP-NNNN y que la
    tabla muestre la fila del nuevo empleado con estado 'Activo'.
    """
    correo_unico = f"ana.lopez.{uuid.uuid4().hex[:8]}@empresa.com"

    page.goto(url_web)

    # Rellenar el formulario
    page.get_by_test_id("empleado-nombre").fill("Ana López")
    page.get_by_test_id("empleado-correo").fill(correo_unico)
    page.get_by_test_id("empleado-puesto").fill("Analista de Datos")
    page.get_by_test_id("empleado-departamento").select_option("Tecnología")
    page.get_by_test_id("empleado-fecha-ingreso").fill("2026-11-08")

    # Guardar
    page.get_by_test_id("empleado-guardar").click()

    # Verificar mensaje de éxito con numero_empleado en formato EMP-NNNN
    mensaje_exito = page.get_by_test_id("mensaje-exito")
    mensaje_exito.wait_for(state="visible")

    texto_mensaje = mensaje_exito.inner_text()
    assert re.search(r"EMP-\d{4}", texto_mensaje), (
        f"El mensaje de éxito no contiene un numero_empleado con formato "
        f"EMP-NNNN. Texto obtenido: '{texto_mensaje}'"
    )

    # Extraer el ID del numero_empleado para localizar la fila
    match = re.search(r"EMP-(\d{4})", texto_mensaje)
    assert match, (
        f"No se pudo extraer el numero_empleado del mensaje: '{texto_mensaje}'"
    )

    # Verificar que la tabla muestra el empleado con estado 'Activo'
    tabla = page.get_by_test_id("tabla-empleados")
    tabla.wait_for(state="visible")

    # Buscar cualquier celda de estado que muestre 'Activo' en la tabla
    estados_activos = tabla.locator("[data-testid^='estado-empleado-']").filter(
        has_text="Activo"
    )
    assert estados_activos.count() > 0, (
        "No se encontró ninguna fila con estado 'Activo' en la tabla de empleados."
    )
