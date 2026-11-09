"""
Backend de gestión de empleados.
FastAPI + SQLAlchemy 2 + SQLite.
"""
from typing import List

from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from esquemas import DEPARTAMENTOS, EmpleadoEntrada, EmpleadoSalida
from modelos import Empleado, crear_tablas, get_db

# Crear tablas al arrancar la aplicación
crear_tablas()

app = FastAPI(title="Gestión de Empleados", version="1.0.0")

# CORS para el frontend en desarrollo (puerto 5173)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _mensaje_error(e: dict) -> str:
    """
    Convierte un error de validación de Pydantic v2 en un mensaje en español.
    - Campos obligatorios ausentes (type == "missing"): indica el nombre del campo.
    - Otros errores: usa el msg del error, eliminando el prefijo "Value error, ".
    """
    tipo = e.get("type", "")
    loc = e.get("loc", ())
    # El último elemento de loc es el nombre del campo (omitir "body" u otros prefijos)
    campo = str(loc[-1]) if loc else ""
    if tipo == "missing" and campo:
        return f"El campo {campo} es obligatorio"
    msg = e.get("msg", "Error de validación")
    # Pydantic v2 prefija los mensajes de validadores con "Value error, "
    if msg.startswith("Value error, "):
        msg = msg[len("Value error, "):]
    return msg


@app.exception_handler(RequestValidationError)
async def validacion_handler(request: Request, exc: RequestValidationError):
    """
    Convierte los errores de validación de Pydantic en respuestas 422
    con el mensaje en español como cadena simple en 'detail'.
    Si hay un solo error, lo devuelve como string; si hay varios, como lista.
    """
    errores = exc.errors()
    if len(errores) == 1:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": _mensaje_error(errores[0])},
        )
    # Varios errores: devuelve lista de {campo, mensaje}
    detalles = []
    for e in errores:
        campo = str(e.get("loc", [""])[-1])
        detalles.append({"campo": campo, "mensaje": _mensaje_error(e)})
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": detalles},
    )


@app.get("/api/salud")
def salud():
    """Verificación de estado del servicio."""
    return {"estado": "ok"}


@app.get("/api/departamentos", response_model=List[str])
def listar_departamentos():
    """Devuelve la lista de departamentos válidos."""
    return DEPARTAMENTOS


@app.post(
    "/api/empleados",
    response_model=EmpleadoSalida,
    status_code=status.HTTP_201_CREATED,
)
def crear_empleado(datos: EmpleadoEntrada, db: Session = Depends(get_db)):
    """Registra un nuevo empleado en la base de datos."""
    # Verificar correo duplicado (la validación de Pydantic ya lo convirtió a minúsculas)
    existente = db.query(Empleado).filter(Empleado.correo == datos.correo).first()
    if existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El correo ya está registrado",
        )

    # Crear el registro
    empleado = Empleado(
        nombre=datos.nombre,
        correo=datos.correo,
        puesto=datos.puesto,
        departamento=datos.departamento,
        fecha_ingreso=datos.fecha_ingreso,
        estado="activo",
    )
    db.add(empleado)
    db.flush()  # Obtener el id generado antes de hacer commit

    # Asignar número de empleado con el id recién generado
    empleado.numero_empleado = f"EMP-{empleado.id:04d}"
    db.commit()
    db.refresh(empleado)

    return empleado


@app.get("/api/empleados", response_model=List[EmpleadoSalida])
def listar_empleados(db: Session = Depends(get_db)):
    """Devuelve todos los empleados registrados."""
    return db.query(Empleado).all()
