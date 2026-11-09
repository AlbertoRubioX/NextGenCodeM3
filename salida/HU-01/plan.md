# Plan de implementación · HU-01 · Registrar empleado

## Modelo de datos

Tabla `empleados` en SQLite (SQLAlchemy 2, modelo `Empleado`):

| Columna | Tipo | Notas |
|---|---|---|
| id | Integer PK autoincrement | |
| numero_empleado | String único | Calculado: EMP-{id:04d} tras insertar |
| nombre | String(80) | 2–80 chars, obligatorio |
| correo | String(120) único | Guardado en minúsculas, solo @empresa.com |
| puesto | String(60) | 2–60 chars, obligatorio |
| departamento | String(40) | Enum: Tecnología/Ventas/Finanzas/RRHH/Operaciones |
| fecha_ingreso | Date | No puede ser futura |
| estado | String(10) | Default "activo" |
| fecha_baja | Date nullable | Solo en estado "baja" |
| creado_en | DateTime | Default now() |

## Endpoints

| Método | Ruta | Descripción | Respuestas |
|---|---|---|---|
| GET | /api/salud | Health check | 200 `{"estado":"ok"}` |
| GET | /api/departamentos | Lista de departamentos | 200 lista |
| POST | /api/empleados | Crear empleado | 201 / 409 / 422 |

Validaciones en Pydantic v2 (`EmpleadoEntrada`): correo lowercase y solo @empresa.com (422), fecha_ingreso <= hoy (422), campos obligatorios (422). Duplicado de correo: 409 `{"detail":"El correo ya está registrado"}`.

## Componentes de React

- `App.jsx` — enruta entre `/` (formulario + tabla) por ahora sin react-router
- `FormularioEmpleado.jsx` — formulario de alta; llama POST `/api/empleados`; muestra `mensaje-exito` o `mensaje-error`
- `TablaEmpleados.jsx` — lista empleados con `tabla-empleados` y filas `fila-empleado-{id}`
- `api.js` — funciones `crearEmpleado()` y `obtenerEmpleados()` usando fetch con rutas relativas

## data-testid

`empleado-nombre`, `empleado-correo`, `empleado-puesto`, `empleado-departamento`, `empleado-fecha-ingreso`, `empleado-guardar`, `mensaje-exito`, `mensaje-error`, `tabla-empleados`, `fila-empleado-{id}`, `numero-empleado-{id}`, `estado-empleado-{id}`

## Archivos a crear o modificar

```
app/
  backend/
    main.py              — FastAPI app, rutas /api/salud, /api/departamentos, /api/empleados
    modelos.py           — SQLAlchemy: clase Empleado + Base + get_db
    esquemas.py          — Pydantic v2: EmpleadoEntrada, EmpleadoSalida
    requirements.txt     — fastapi, uvicorn, sqlalchemy, pydantic
  frontend/
    package.json         — React + Vite
    vite.config.js       — proxy /api → localhost:8000
    index.html
    src/
      main.jsx
      App.jsx
      components/
        FormularioEmpleado.jsx
        TablaEmpleados.jsx
      api.js
```
