"""Pruebas E2E para HU-02: Directorio de empleados (Playwright)."""
import uuid

import pytest


# ---------------------------------------------------------------------------
# CP-02: Listar todos los empleados del directorio (E2E)
# ---------------------------------------------------------------------------

def test_cp02_listar_empleados_en_tabla(page, url_web):
    """CP-02: Listar todos los empleados del directorio.

    Navega al directorio y verifica que la tabla es visible y que las filas
    de Ana López (EMP-0001, Activo) y Pedro García (Baja) están presentes.
    """
    page.goto(url_web)

    # Verificar que la tabla de empleados es visible
    tabla = page.get_by_test_id("tabla-empleados")
    tabla.wait_for(state="visible")
    assert tabla.is_visible(), "La tabla de empleados no es visible."

    # Localizar la fila de Ana López (EMP-0001) a través del numero_empleado
    # Se busca la celda con numero EMP-0001 para obtener el id de fila
    numero_emp_0001 = page.locator("[data-testid^='numero-empleado-']").filter(
        has_text="EMP-0001"
    )
    numero_emp_0001.wait_for(state="visible", timeout=10000)
    assert numero_emp_0001.count() > 0, (
        "No se encontró ningún elemento con numero_empleado='EMP-0001'."
    )

    # Extraer el id del data-testid del elemento numero-empleado-{id}
    testid_numero = numero_emp_0001.first.get_attribute("data-testid")
    # testid_numero es algo como "numero-empleado-1"
    id_emp_0001 = testid_numero.replace("numero-empleado-", "")

    # Verificar la fila de Ana López
    fila_ana = page.get_by_test_id(f"fila-empleado-{id_emp_0001}")
    assert fila_ana.is_visible(), (
        f"La fila 'fila-empleado-{id_emp_0001}' no es visible."
    )
    assert "Ana López" in fila_ana.inner_text(), (
        f"La fila {id_emp_0001} no contiene el texto 'Ana López'."
    )

    # Verificar estado Activo para Ana López
    estado_ana = page.get_by_test_id(f"estado-empleado-{id_emp_0001}")
    assert "Activo" in estado_ana.inner_text(), (
        f"Se esperaba estado 'Activo' para Ana López, "
        f"obtenido: '{estado_ana.inner_text()}'."
    )

    # Localizar a Pedro García en la tabla (con estado Baja)
    filas = tabla.locator("[data-testid^='fila-empleado-']")
    filas.first.wait_for(state="visible", timeout=10000)

    fila_pedro = None
    for i in range(filas.count()):
        fila = filas.nth(i)
        if "Pedro García" in fila.inner_text():
            fila_pedro = fila
            break

    assert fila_pedro is not None, (
        "No se encontró ninguna fila con el texto 'Pedro García' en la tabla."
    )

    # Extraer el id de la fila de Pedro García
    testid_fila_pedro = fila_pedro.get_attribute("data-testid")
    id_pedro = testid_fila_pedro.replace("fila-empleado-", "")

    estado_pedro = page.get_by_test_id(f"estado-empleado-{id_pedro}")
    assert "Baja" in estado_pedro.inner_text(), (
        f"Se esperaba estado 'Baja' para Pedro García, "
        f"obtenido: '{estado_pedro.inner_text()}'."
    )


# ---------------------------------------------------------------------------
# CP-04: Buscar empleado por nombre sin distinguir mayúsculas (E2E)
# ---------------------------------------------------------------------------

def test_cp04_buscar_por_nombre_case_insensitive(page, url_web):
    """CP-04: Buscar empleado por nombre sin distinguir mayúsculas.

    Escribe 'ana lópez' en el campo de búsqueda y verifica que la tabla
    muestra exactamente 1 fila con el empleado 'Ana López'.
    """
    page.goto(url_web)

    # Esperar a que la tabla y el campo de búsqueda estén disponibles
    page.get_by_test_id("tabla-empleados").wait_for(state="visible")

    campo_busqueda = page.get_by_test_id("buscar-empleados")
    campo_busqueda.wait_for(state="visible")
    campo_busqueda.fill("ana lópez")

    # Esperar a que la tabla se actualice
    tabla = page.get_by_test_id("tabla-empleados")
    tabla.wait_for(state="visible")

    # Contar filas de empleados visibles
    filas = tabla.locator("[data-testid^='fila-empleado-']")
    page.wait_for_timeout(500)  # breve espera para renderizado
    cantidad = filas.count()
    assert cantidad == 1, (
        f"Se esperaba exactamente 1 fila de empleado, se obtuvieron {cantidad}."
    )

    # Verificar que la fila contiene 'Ana López'
    fila = filas.first
    assert "Ana López" in fila.inner_text(), (
        f"La fila visible no contiene el texto 'Ana López'. "
        f"Contenido: '{fila.inner_text()}'."
    )


# ---------------------------------------------------------------------------
# CP-06: Buscar empleado por correo en mayúsculas (E2E)
# ---------------------------------------------------------------------------

def test_cp06_buscar_por_correo_mayusculas(page, url_web):
    """CP-06: Buscar empleado por correo en mayúsculas.

    Escribe 'ANA.LOPEZ@EMPRESA.COM' en el campo de búsqueda y verifica que
    la tabla muestra exactamente 1 fila con el correo 'ana.lopez@empresa.com'.
    """
    page.goto(url_web)

    page.get_by_test_id("tabla-empleados").wait_for(state="visible")

    campo_busqueda = page.get_by_test_id("buscar-empleados")
    campo_busqueda.wait_for(state="visible")
    campo_busqueda.fill("ANA.LOPEZ@EMPRESA.COM")

    tabla = page.get_by_test_id("tabla-empleados")
    tabla.wait_for(state="visible")

    filas = tabla.locator("[data-testid^='fila-empleado-']")
    page.wait_for_timeout(500)
    cantidad = filas.count()
    assert cantidad == 1, (
        f"Se esperaba exactamente 1 fila de empleado, se obtuvieron {cantidad}."
    )

    fila = filas.first
    assert "ana.lopez@empresa.com" in fila.inner_text().lower(), (
        f"La fila visible no contiene el correo 'ana.lopez@empresa.com'. "
        f"Contenido: '{fila.inner_text()}'."
    )


# ---------------------------------------------------------------------------
# CP-08: Filtrar empleados por departamento (E2E)
# ---------------------------------------------------------------------------

def test_cp08_filtrar_por_departamento(page, url_web):
    """CP-08: Filtrar empleados por departamento.

    Selecciona 'Finanzas' en el desplegable de filtro y verifica que
    todas las filas visibles muestran 'Finanzas' y ninguna muestra 'Ventas'.
    """
    page.goto(url_web)

    page.get_by_test_id("tabla-empleados").wait_for(state="visible")

    filtro = page.get_by_test_id("filtro-departamento")
    filtro.wait_for(state="visible")
    filtro.select_option("Finanzas")

    tabla = page.get_by_test_id("tabla-empleados")
    tabla.wait_for(state="visible")
    page.wait_for_timeout(500)

    filas = tabla.locator("[data-testid^='fila-empleado-']")
    cantidad = filas.count()
    assert cantidad > 0, (
        "No se encontraron filas de empleados después de filtrar por 'Finanzas'."
    )

    for i in range(cantidad):
        fila = filas.nth(i)
        texto_fila = fila.inner_text()
        assert "Finanzas" in texto_fila, (
            f"La fila {i} no pertenece al departamento 'Finanzas'. "
            f"Contenido: '{texto_fila}'."
        )
        assert "Ventas" not in texto_fila, (
            f"La fila {i} contiene 'Ventas' cuando se esperaba solo 'Finanzas'. "
            f"Contenido: '{texto_fila}'."
        )


# ---------------------------------------------------------------------------
# CP-10: Búsqueda sin resultados muestra mensaje informativo (E2E)
# ---------------------------------------------------------------------------

def test_cp10_busqueda_sin_resultados(page, url_web):
    """CP-10: Búsqueda sin resultados muestra mensaje informativo.

    Escribe 'zzznoencontrado' en el campo de búsqueda y verifica que la
    tabla no muestra filas de empleados y que el elemento 'sin-resultados'
    es visible con un mensaje informativo.
    """
    page.goto(url_web)

    page.get_by_test_id("tabla-empleados").wait_for(state="visible")

    campo_busqueda = page.get_by_test_id("buscar-empleados")
    campo_busqueda.wait_for(state="visible")
    campo_busqueda.fill("zzznoencontrado")

    page.wait_for_timeout(500)

    tabla = page.get_by_test_id("tabla-empleados")
    filas = tabla.locator("[data-testid^='fila-empleado-']")
    assert filas.count() == 0, (
        f"Se esperaba 0 filas de empleados, se obtuvieron {filas.count()}."
    )

    sin_resultados = page.get_by_test_id("sin-resultados")
    sin_resultados.wait_for(state="visible", timeout=5000)
    assert sin_resultados.is_visible(), (
        "El elemento 'sin-resultados' no es visible."
    )
    assert len(sin_resultados.inner_text().strip()) > 0, (
        "El elemento 'sin-resultados' está visible pero no contiene texto."
    )


# ---------------------------------------------------------------------------
# CP-12: Filtro por departamento sin resultados muestra mensaje informativo (E2E)
# ---------------------------------------------------------------------------

def test_cp12_filtro_departamento_sin_resultados(page, url_web):
    """CP-12: Filtro por departamento sin resultados muestra mensaje informativo.

    Selecciona 'Operaciones' en el desplegable y verifica que la tabla no
    muestra filas de empleados y que el elemento 'sin-resultados' es visible.
    """
    page.goto(url_web)

    page.get_by_test_id("tabla-empleados").wait_for(state="visible")

    filtro = page.get_by_test_id("filtro-departamento")
    filtro.wait_for(state="visible")
    filtro.select_option("Operaciones")

    page.wait_for_timeout(500)

    tabla = page.get_by_test_id("tabla-empleados")
    filas = tabla.locator("[data-testid^='fila-empleado-']")
    assert filas.count() == 0, (
        f"Se esperaba 0 filas de empleados para 'Operaciones', "
        f"se obtuvieron {filas.count()}."
    )

    sin_resultados = page.get_by_test_id("sin-resultados")
    sin_resultados.wait_for(state="visible", timeout=5000)
    assert sin_resultados.is_visible(), (
        "El elemento 'sin-resultados' no es visible."
    )
    assert len(sin_resultados.inner_text().strip()) > 0, (
        "El elemento 'sin-resultados' está visible pero no contiene texto."
    )


# ---------------------------------------------------------------------------
# CP-14: El directorio muestra empleados dados de baja (E2E)
# ---------------------------------------------------------------------------

def test_cp14_directorio_muestra_empleados_baja(page, url_web):
    """CP-14: El directorio muestra empleados dados de baja.

    Navega al directorio y verifica que la tabla es visible, que Pedro García
    aparece en alguna fila y que su estado indica 'Baja'.
    """
    page.goto(url_web)

    tabla = page.get_by_test_id("tabla-empleados")
    tabla.wait_for(state="visible")
    assert tabla.is_visible(), "La tabla de empleados no es visible."

    filas = tabla.locator("[data-testid^='fila-empleado-']")
    filas.first.wait_for(state="visible", timeout=10000)

    fila_pedro = None
    for i in range(filas.count()):
        fila = filas.nth(i)
        if "Pedro García" in fila.inner_text():
            fila_pedro = fila
            break

    assert fila_pedro is not None, (
        "No se encontró ninguna fila con el texto 'Pedro García' en la tabla."
    )

    testid_fila = fila_pedro.get_attribute("data-testid")
    id_pedro = testid_fila.replace("fila-empleado-", "")

    estado_pedro = page.get_by_test_id(f"estado-empleado-{id_pedro}")
    texto_estado = estado_pedro.inner_text()
    assert "Baja" in texto_estado, (
        f"Se esperaba que el estado de Pedro García fuera 'Baja', "
        f"obtenido: '{texto_estado}'."
    )
