"""Pruebas de API para HU-02: Directorio de empleados (búsqueda y filtros)."""
import uuid

import httpx
import pytest


# ---------------------------------------------------------------------------
# Utilidad: crear un empleado de apoyo con correo único
# ---------------------------------------------------------------------------

def _crear_empleado(url_api, nombre, correo, puesto, departamento, estado=None):
    """Crea un empleado y devuelve el cuerpo de la respuesta."""
    payload = {
        "nombre": nombre,
        "correo": correo,
        "puesto": puesto,
        "departamento": departamento,
        "fecha_ingreso": "2024-01-15",
    }
    r = httpx.post(f"{url_api}/api/empleados", json=payload)
    assert r.status_code == 201, (
        f"Fallo al crear empleado de precondición '{nombre}': {r.text}"
    )
    return r.json()


# ---------------------------------------------------------------------------
# CP-01: Listar todos los empleados del directorio (API)
# ---------------------------------------------------------------------------

def test_cp01_listar_todos_los_empleados(url_api):
    """CP-01: Listar todos los empleados del directorio.

    Crea dos empleados (uno activo y uno dado de baja) y verifica que
    GET /api/empleados devuelve HTTP 200, una lista JSON y que ambos
    empleados aparecen con los datos correctos.
    """
    sufijo = uuid.uuid4().hex[:8]
    correo_ana = f"ana.lopez.{sufijo}@empresa.com"
    correo_pedro = f"pedro.garcia.{sufijo}@empresa.com"

    emp_ana = _crear_empleado(
        url_api,
        nombre="Ana López",
        correo=correo_ana,
        puesto="Analista de Datos",
        departamento="Tecnología",
    )
    emp_pedro = _crear_empleado(
        url_api,
        nombre="Pedro García",
        correo=correo_pedro,
        puesto="Ejecutivo de Ventas",
        departamento="Ventas",
    )

    # Dar de baja a Pedro García si la API lo permite
    id_pedro = emp_pedro.get("id")
    if id_pedro:
        httpx.patch(
            f"{url_api}/api/empleados/{id_pedro}/baja",
            json={"fecha_baja": "2024-06-01"},
        )

    response = httpx.get(f"{url_api}/api/empleados")

    assert response.status_code == 200, (
        f"Se esperaba 200, se obtuvo {response.status_code}. Cuerpo: {response.text}"
    )

    cuerpo = response.json()

    # Puede ser lista directa o dict con clave 'empleados'
    empleados = cuerpo if isinstance(cuerpo, list) else cuerpo.get("empleados", cuerpo)
    assert isinstance(empleados, list), (
        f"Se esperaba que el cuerpo fuera una lista o contuviera una lista. "
        f"Cuerpo: {cuerpo}"
    )

    nums_empleado = [e.get("numero_empleado") for e in empleados]
    numero_ana = emp_ana.get("numero_empleado")
    assert numero_ana in nums_empleado, (
        f"No se encontró el numero_empleado '{numero_ana}' (Ana López) en la lista."
    )

    # Verificar que el registro de Ana López tiene los campos correctos
    registro_ana = next(
        (e for e in empleados if e.get("numero_empleado") == numero_ana), None
    )
    assert registro_ana is not None
    assert registro_ana.get("nombre") == "Ana López", (
        f"Nombre esperado 'Ana López', obtenido '{registro_ana.get('nombre')}'."
    )
    assert registro_ana.get("puesto") == "Analista de Datos", (
        f"Puesto esperado 'Analista de Datos', obtenido '{registro_ana.get('puesto')}'."
    )
    assert registro_ana.get("departamento") == "Tecnología", (
        f"Departamento esperado 'Tecnología', obtenido '{registro_ana.get('departamento')}'."
    )
    assert registro_ana.get("estado") == "activo", (
        f"Estado esperado 'activo', obtenido '{registro_ana.get('estado')}'."
    )

    # Verificar que Pedro García aparece (con cualquier estado)
    registro_pedro = next(
        (e for e in empleados if e.get("nombre") == "Pedro García"
         and e.get("correo") == correo_pedro),
        None,
    )
    assert registro_pedro is not None, (
        "Pedro García no aparece en el listado de empleados."
    )


# ---------------------------------------------------------------------------
# CP-03: Buscar empleado por nombre sin distinguir mayúsculas (API)
# ---------------------------------------------------------------------------

def test_cp03_buscar_por_nombre_case_insensitive(url_api):
    """CP-03: Buscar empleado por nombre sin distinguir mayúsculas.

    Crea un empleado con nombre 'Ana López' y busca con 'ana lópez' en
    minúsculas. Verifica HTTP 200, exactamente 1 resultado y nombre correcto.
    """
    sufijo = uuid.uuid4().hex[:8]
    correo = f"ana.lopez.{sufijo}@empresa.com"
    _crear_empleado(
        url_api,
        nombre="Ana López",
        correo=correo,
        puesto="Analista de Datos",
        departamento="Tecnología",
    )

    response = httpx.get(f"{url_api}/api/empleados", params={"q": "ana lópez"})

    assert response.status_code == 200, (
        f"Se esperaba 200, se obtuvo {response.status_code}. Cuerpo: {response.text}"
    )

    cuerpo = response.json()
    empleados = cuerpo if isinstance(cuerpo, list) else cuerpo.get("empleados", cuerpo)
    assert isinstance(empleados, list), (
        f"Se esperaba una lista de empleados. Cuerpo: {cuerpo}"
    )

    # Filtrar los resultados para solo incluir el que creamos en este test
    resultados = [e for e in empleados if e.get("correo") == correo]
    assert len(resultados) == 1, (
        f"Se esperaba exactamente 1 resultado para el correo '{correo}', "
        f"se obtuvieron {len(resultados)}."
    )
    assert resultados[0].get("nombre") == "Ana López", (
        f"Nombre esperado 'Ana López', obtenido '{resultados[0].get('nombre')}'."
    )


# ---------------------------------------------------------------------------
# CP-05: Buscar empleado por correo en mayúsculas (API)
# ---------------------------------------------------------------------------

def test_cp05_buscar_por_correo_mayusculas(url_api):
    """CP-05: Buscar empleado por correo en mayúsculas.

    Crea un empleado con correo en minúsculas y busca con el correo en
    mayúsculas. Verifica HTTP 200, exactamente 1 resultado y correo correcto.
    """
    sufijo = uuid.uuid4().hex[:8]
    correo = f"ana.lopez.{sufijo}@empresa.com"
    _crear_empleado(
        url_api,
        nombre="Ana López",
        correo=correo,
        puesto="Analista de Datos",
        departamento="Tecnología",
    )

    response = httpx.get(
        f"{url_api}/api/empleados", params={"q": correo.upper()}
    )

    assert response.status_code == 200, (
        f"Se esperaba 200, se obtuvo {response.status_code}. Cuerpo: {response.text}"
    )

    cuerpo = response.json()
    empleados = cuerpo if isinstance(cuerpo, list) else cuerpo.get("empleados", cuerpo)
    assert isinstance(empleados, list), (
        f"Se esperaba una lista de empleados. Cuerpo: {cuerpo}"
    )

    resultados = [e for e in empleados if e.get("correo") == correo]
    assert len(resultados) == 1, (
        f"Se esperaba exactamente 1 resultado para correo '{correo}', "
        f"se obtuvieron {len(resultados)}."
    )
    assert resultados[0].get("correo") == correo, (
        f"Correo esperado '{correo}', obtenido '{resultados[0].get('correo')}'."
    )


# ---------------------------------------------------------------------------
# CP-07: Filtrar empleados por departamento (API)
# ---------------------------------------------------------------------------

def test_cp07_filtrar_por_departamento(url_api):
    """CP-07: Filtrar empleados por departamento.

    Crea empleados en 'Finanzas' y 'Ventas' y verifica que el filtro
    por 'Finanzas' devuelve solo empleados de ese departamento.
    """
    sufijo = uuid.uuid4().hex[:8]
    _crear_empleado(
        url_api,
        nombre=f"Empleado Finanzas {sufijo}",
        correo=f"finanzas.{sufijo}@empresa.com",
        puesto="Contador",
        departamento="Finanzas",
    )
    _crear_empleado(
        url_api,
        nombre=f"Empleado Ventas {sufijo}",
        correo=f"ventas.{sufijo}@empresa.com",
        puesto="Ejecutivo de Ventas",
        departamento="Ventas",
    )

    response = httpx.get(
        f"{url_api}/api/empleados", params={"departamento": "Finanzas"}
    )

    assert response.status_code == 200, (
        f"Se esperaba 200, se obtuvo {response.status_code}. Cuerpo: {response.text}"
    )

    cuerpo = response.json()
    empleados = cuerpo if isinstance(cuerpo, list) else cuerpo.get("empleados", cuerpo)
    assert isinstance(empleados, list), (
        f"Se esperaba una lista de empleados. Cuerpo: {cuerpo}"
    )

    assert len(empleados) > 0, (
        "Se esperaba al menos 1 empleado en el departamento 'Finanzas'."
    )

    departamentos = {e.get("departamento") for e in empleados}
    assert departamentos == {"Finanzas"}, (
        f"Se esperaba que todos los empleados fueran de 'Finanzas', "
        f"pero se encontraron departamentos: {departamentos}."
    )

    nombres_ventas = [
        e.get("nombre") for e in empleados if e.get("departamento") == "Ventas"
    ]
    assert len(nombres_ventas) == 0, (
        f"Se encontraron empleados de 'Ventas' en el filtro de 'Finanzas': "
        f"{nombres_ventas}."
    )


# ---------------------------------------------------------------------------
# CP-09: Búsqueda sin resultados muestra mensaje informativo (API)
# ---------------------------------------------------------------------------

def test_cp09_busqueda_sin_resultados(url_api):
    """CP-09: Búsqueda sin resultados muestra mensaje informativo.

    Busca con una cadena inexistente y verifica HTTP 200, lista vacía y
    campo de mensaje informativo en la respuesta.
    """
    response = httpx.get(
        f"{url_api}/api/empleados", params={"q": "zzznoencontrado"}
    )

    assert response.status_code == 200, (
        f"Se esperaba 200, se obtuvo {response.status_code}. Cuerpo: {response.text}"
    )

    cuerpo = response.json()
    empleados = cuerpo if isinstance(cuerpo, list) else cuerpo.get("empleados", [])
    assert isinstance(empleados, list), (
        f"Se esperaba una lista de empleados. Cuerpo: {cuerpo}"
    )
    assert len(empleados) == 0, (
        f"Se esperaba lista vacía, se obtuvieron {len(empleados)} empleados."
    )

    # Cuando el cuerpo es dict debe incluir un mensaje informativo
    if isinstance(cuerpo, dict):
        tiene_mensaje = any(
            isinstance(v, str) and len(v) > 0
            for k, v in cuerpo.items()
            if k != "empleados"
        )
        assert tiene_mensaje, (
            f"Se esperaba un campo de mensaje informativo en la respuesta. "
            f"Cuerpo: {cuerpo}"
        )


# ---------------------------------------------------------------------------
# CP-11: Filtro por departamento sin resultados muestra mensaje informativo (API)
# ---------------------------------------------------------------------------

def test_cp11_filtro_departamento_sin_resultados(url_api):
    """CP-11: Filtro por departamento sin resultados muestra mensaje informativo.

    Filtra por 'Operaciones' (departamento sin empleados) y verifica
    HTTP 200, lista vacía y campo de mensaje informativo.
    """
    response = httpx.get(
        f"{url_api}/api/empleados", params={"departamento": "Operaciones"}
    )

    assert response.status_code == 200, (
        f"Se esperaba 200, se obtuvo {response.status_code}. Cuerpo: {response.text}"
    )

    cuerpo = response.json()
    empleados = cuerpo if isinstance(cuerpo, list) else cuerpo.get("empleados", [])
    assert isinstance(empleados, list), (
        f"Se esperaba una lista de empleados. Cuerpo: {cuerpo}"
    )
    assert len(empleados) == 0, (
        f"Se esperaba lista vacía para departamento 'Operaciones', "
        f"se obtuvieron {len(empleados)} empleados."
    )

    if isinstance(cuerpo, dict):
        tiene_mensaje = any(
            isinstance(v, str) and len(v) > 0
            for k, v in cuerpo.items()
            if k != "empleados"
        )
        assert tiene_mensaje, (
            f"Se esperaba un campo de mensaje informativo en la respuesta. "
            f"Cuerpo: {cuerpo}"
        )


# ---------------------------------------------------------------------------
# CP-13: El directorio muestra empleados dados de baja (API)
# ---------------------------------------------------------------------------

def test_cp13_directorio_incluye_empleados_baja(url_api):
    """CP-13: El directorio muestra empleados dados de baja.

    Crea un empleado y lo da de baja, luego verifica que GET /api/empleados
    devuelve HTTP 200 y que el empleado aparece con estado='baja'.
    """
    sufijo = uuid.uuid4().hex[:8]
    correo_pedro = f"pedro.garcia.{sufijo}@empresa.com"

    emp = _crear_empleado(
        url_api,
        nombre="Pedro García",
        correo=correo_pedro,
        puesto="Ejecutivo de Ventas",
        departamento="Ventas",
    )
    id_pedro = emp.get("id")
    assert id_pedro is not None, (
        f"El empleado creado no tiene campo 'id'. Respuesta: {emp}"
    )

    # Dar de baja al empleado
    r_baja = httpx.patch(
        f"{url_api}/api/empleados/{id_pedro}/baja",
        json={"fecha_baja": "2024-06-01"},
    )
    assert r_baja.status_code in (200, 204), (
        f"Fallo al dar de baja al empleado: {r_baja.text}"
    )

    response = httpx.get(f"{url_api}/api/empleados")

    assert response.status_code == 200, (
        f"Se esperaba 200, se obtuvo {response.status_code}. Cuerpo: {response.text}"
    )

    cuerpo = response.json()
    empleados = cuerpo if isinstance(cuerpo, list) else cuerpo.get("empleados", cuerpo)
    assert isinstance(empleados, list), (
        f"Se esperaba una lista de empleados. Cuerpo: {cuerpo}"
    )

    registro_pedro = next(
        (e for e in empleados if e.get("correo") == correo_pedro), None
    )
    assert registro_pedro is not None, (
        f"Pedro García (correo: {correo_pedro}) no aparece en el listado."
    )
    assert registro_pedro.get("estado") == "baja", (
        f"Estado esperado 'baja', obtenido '{registro_pedro.get('estado')}'."
    )
