"""
Backend de gestión de empleados.
FastAPI + SQLAlchemy 2 + SQLite.
"""
import unicodedata
from datetime import date as _date
from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException, Query, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from esquemas import DEPARTAMENTOS, EmpleadoEntrada, EmpleadoListaSalida, EmpleadoSalida
from modelos import Empleado, crear_tablas, get_db

# Crear tablas al arrancar la aplicación
crear_tablas()

app = FastAPI(title="Gestión de Empleados", version="1.0.0")


def _sembrar_datos_iniciales() -> None:
    """
    Siembra la base de datos con empleados de prueba si está vacía.
    Incluye a Pedro García con estado 'baja' para los escenarios de prueba
    que verifican la visualización de empleados dados de baja.
    """
    from modelos import engine
    with Session(engine) as db:
        if db.query(Empleado).count() > 0:
            return  # Ya hay datos, no sembrar de nuevo

        empleados_semilla = [
            # EMP-0001: Ana López – Tecnología, activo
            {
                "nombre": "Ana López",
                "correo": "ana.lopez@empresa.com",
                "puesto": "Analista de Datos",
                "departamento": "Tecnología",
                "fecha_ingreso": _date(2022, 3, 15),
                "estado": "activo",
                "fecha_baja": None,
            },
            # EMP-0002: Pedro García – Ventas, baja
            {
                "nombre": "Pedro García",
                "correo": "pedro.garcia@empresa.com",
                "puesto": "Ejecutivo de Ventas",
                "departamento": "Ventas",
                "fecha_ingreso": _date(2021, 6, 1),
                "estado": "baja",
                "fecha_baja": _date(2024, 1, 10),
            },
            # EMP-0003 a EMP-0014: empleados adicionales para completar el directorio
            {
                "nombre": "Carlos Mendoza",
                "correo": "carlos.mendoza@empresa.com",
                "puesto": "Desarrollador Backend",
                "departamento": "Tecnología",
                "fecha_ingreso": _date(2020, 9, 1),
                "estado": "activo",
                "fecha_baja": None,
            },
            {
                "nombre": "Laura Sánchez",
                "correo": "laura.sanchez@empresa.com",
                "puesto": "Contadora",
                "departamento": "Finanzas",
                "fecha_ingreso": _date(2019, 4, 20),
                "estado": "activo",
                "fecha_baja": None,
            },
            {
                "nombre": "Miguel Torres",
                "correo": "miguel.torres@empresa.com",
                "puesto": "Gerente de Ventas",
                "departamento": "Ventas",
                "fecha_ingreso": _date(2018, 11, 5),
                "estado": "activo",
                "fecha_baja": None,
            },
            {
                "nombre": "Sofía Ramírez",
                "correo": "sofia.ramirez@empresa.com",
                "puesto": "Especialista en RRHH",
                "departamento": "Recursos Humanos",
                "fecha_ingreso": _date(2021, 2, 14),
                "estado": "activo",
                "fecha_baja": None,
            },
            {
                "nombre": "Diego Flores",
                "correo": "diego.flores@empresa.com",
                "puesto": "Desarrollador Frontend",
                "departamento": "Tecnología",
                "fecha_ingreso": _date(2022, 7, 18),
                "estado": "activo",
                "fecha_baja": None,
            },
            {
                "nombre": "Valentina Cruz",
                "correo": "valentina.cruz@empresa.com",
                "puesto": "Analista Financiera",
                "departamento": "Finanzas",
                "fecha_ingreso": _date(2020, 5, 30),
                "estado": "activo",
                "fecha_baja": None,
            },
            {
                "nombre": "Roberto Jiménez",
                "correo": "roberto.jimenez@empresa.com",
                "puesto": "Asesor Comercial",
                "departamento": "Ventas",
                "fecha_ingreso": _date(2023, 1, 9),
                "estado": "activo",
                "fecha_baja": None,
            },
            {
                "nombre": "Elena Vargas",
                "correo": "elena.vargas@empresa.com",
                "puesto": "Reclutadora",
                "departamento": "Recursos Humanos",
                "fecha_ingreso": _date(2019, 8, 22),
                "estado": "activo",
                "fecha_baja": None,
            },
            {
                "nombre": "Francisco Morales",
                "correo": "francisco.morales@empresa.com",
                "puesto": "Arquitecto de Software",
                "departamento": "Tecnología",
                "fecha_ingreso": _date(2017, 3, 12),
                "estado": "activo",
                "fecha_baja": None,
            },
            {
                "nombre": "Patricia Reyes",
                "correo": "patricia.reyes@empresa.com",
                "puesto": "Directora de Finanzas",
                "departamento": "Finanzas",
                "fecha_ingreso": _date(2016, 10, 1),
                "estado": "activo",
                "fecha_baja": None,
            },
            {
                "nombre": "Andrés Castillo",
                "correo": "andres.castillo@empresa.com",
                "puesto": "Coordinador de RRHH",
                "departamento": "Recursos Humanos",
                "fecha_ingreso": _date(2020, 12, 7),
                "estado": "activo",
                "fecha_baja": None,
            },
            {
                "nombre": "Isabel Ortega",
                "correo": "isabel.ortega@empresa.com",
                "puesto": "Ejecutiva de Ventas",
                "departamento": "Ventas",
                "fecha_ingreso": _date(2022, 4, 25),
                "estado": "activo",
                "fecha_baja": None,
            },
        ]

        for i, datos in enumerate(empleados_semilla, start=1):
            empleado = Empleado(
                nombre=datos["nombre"],
                correo=datos["correo"],
                puesto=datos["puesto"],
                departamento=datos["departamento"],
                fecha_ingreso=datos["fecha_ingreso"],
                estado=datos["estado"],
                fecha_baja=datos["fecha_baja"],
            )
            db.add(empleado)
            db.flush()
            empleado.numero_empleado = f"EMP-{empleado.id:04d}"

        db.commit()


# Sembrar datos iniciales al arrancar si la base de datos está vacía
_sembrar_datos_iniciales()

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


@app.patch(
    "/api/empleados/{id}/baja",
    response_model=EmpleadoSalida,
    status_code=status.HTTP_200_OK,
)
def dar_de_baja(id: int, db: Session = Depends(get_db)):
    """Cambia el estado del empleado a 'baja' y registra la fecha de baja."""
    empleado = db.get(Empleado, id)
    if not empleado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Empleado no encontrado",
        )
    if empleado.estado == "baja":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El empleado ya está dado de baja",
        )
    empleado.estado = "baja"
    empleado.fecha_baja = _date.today()
    db.commit()
    db.refresh(empleado)
    return empleado


@app.get("/api/empleados", response_model=EmpleadoListaSalida)
def listar_empleados(
    q: Optional[str] = Query(default=None, description="Busca por nombre o correo (coincidencia parcial, sin distinción de mayúsculas ni acentos)"),
    departamento: Optional[str] = Query(default=None, description="Filtra exacto por departamento"),
    db: Session = Depends(get_db),
):
    """Devuelve empleados con filtros opcionales de búsqueda y departamento."""
    consulta = db.query(Empleado)

    # El filtro de departamento se aplica en la capa SQL (es una comparación exacta).
    if departamento:
        consulta = consulta.filter(Empleado.departamento == departamento)

    lista = consulta.all()

    # El filtro de texto se aplica en Python para manejar correctamente
    # la insensibilidad a mayúsculas y acentos en Unicode.
    if q:
        def _normalizar(texto: str) -> str:
            """Elimina acentos y pasa a minúsculas para comparación insensible."""
            sin_acentos = unicodedata.normalize("NFD", texto)
            sin_acentos = "".join(c for c in sin_acentos if unicodedata.category(c) != "Mn")
            return sin_acentos.lower()

        termino = _normalizar(q)
        lista = [
            emp for emp in lista
            if termino in _normalizar(emp.nombre) or termino in _normalizar(emp.correo)
        ]

    mensaje = ""
    if not lista:
        mensaje = "No se encontraron resultados"

    return EmpleadoListaSalida(empleados=lista, mensaje=mensaje)
