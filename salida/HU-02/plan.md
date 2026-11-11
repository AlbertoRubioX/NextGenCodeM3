# Plan HU-02 · Consultar el directorio de empleados

## Modelo de datos
Sin cambios de esquema. El modelo `Empleado` y `EmpleadoSalida` existentes son suficientes.
Se agrega `EmpleadoListaSalida` en `esquemas.py` para envolver la respuesta con `empleados` + `mensaje`.

## Endpoints
Modificar `GET /api/empleados` en `main.py`:
- Parámetro opcional `q: str | None` — busca por coincidencia parcial en `nombre` o `correo` (case-insensitive con `LOWER()`).
- Parámetro opcional `departamento: str | None` — filtra exacto por departamento.
- Respuesta: `{"empleados": [...], "mensaje": ""}`. Si la lista queda vacía, `mensaje` = `"No se encontraron resultados"`.
- Siempre HTTP 200; empleados de baja siempre incluidos.

## Componentes de React
**`TablaEmpleados.jsx`** — recibe `empleados` y `mensaje`; elimina el renderizado condicional actual; muestra `sin-resultados` cuando `empleados` está vacío y hay mensaje.

**`FiltrosDirectorio.jsx`** (nuevo) — contiene el campo de texto `buscar-empleados` y el `<select>` `filtro-departamento`; llama a `onFiltrar({ q, departamento })` en cada cambio con debounce de 300 ms.

**`App.jsx`** — agrega estado `filtros`; pasa `q` y `departamento` a `obtenerEmpleados`; pasa `empleados` y `mensaje` a `TablaEmpleados`; renderiza `<FiltrosDirectorio>`.

## api.js
Actualizar `obtenerEmpleados(params = {})` para construir `URLSearchParams` con `q` y `departamento` cuando se indiquen. La respuesta ahora devuelve `{ empleados, mensaje }`.

## data-testid
| Elemento | data-testid |
|---|---|
| Campo de búsqueda | `buscar-empleados` |
| Selector de departamento | `filtro-departamento` |
| Tabla | `tabla-empleados` |
| Fila por id | `fila-empleado-{id}` |
| Número de empleado | `numero-empleado-{id}` |
| Estado por fila | `estado-empleado-{id}` (texto «Activo» o «Baja») |
| Sin resultados | `sin-resultados` |

## Archivos a crear o modificar
| Acción | Archivo |
|---|---|
| Modificar | `app/backend/main.py` — ampliar `GET /api/empleados` con `q`, `departamento` y respuesta envuelta |
| Modificar | `app/backend/esquemas.py` — agregar `EmpleadoListaSalida` |
| Modificar | `app/frontend/src/api.js` — aceptar parámetros y leer `{ empleados, mensaje }` |
| Modificar | `app/frontend/src/components/TablaEmpleados.jsx` — recibir `mensaje`, mostrar `sin-resultados` |
| Crear | `app/frontend/src/components/FiltrosDirectorio.jsx` |
| Modificar | `app/frontend/src/App.jsx` — estado de filtros, orquestar búsqueda y filtro |
