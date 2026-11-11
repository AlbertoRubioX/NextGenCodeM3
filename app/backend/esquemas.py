"""
Esquemas Pydantic v2 para la gestión de empleados.
"""
from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, field_validator, model_validator

DEPARTAMENTOS = [
    "Tecnología",
    "Ventas",
    "Finanzas",
    "Recursos Humanos",
    "Operaciones",
]


class EmpleadoEntrada(BaseModel):
    """Datos que el cliente envía para registrar un empleado."""

    nombre: str
    correo: str
    puesto: str
    departamento: str
    fecha_ingreso: date

    @field_validator("nombre")
    @classmethod
    def validar_nombre(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 2 or len(v) > 80:
            raise ValueError("El nombre debe tener entre 2 y 80 caracteres")
        return v

    @field_validator("correo")
    @classmethod
    def validar_correo(cls, v: str) -> str:
        v = v.strip().lower()
        if not v.endswith("@empresa.com"):
            raise ValueError("Usa el correo corporativo @empresa.com")
        return v

    @field_validator("puesto")
    @classmethod
    def validar_puesto(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 2 or len(v) > 60:
            raise ValueError("El puesto debe tener entre 2 y 60 caracteres")
        return v

    @field_validator("departamento")
    @classmethod
    def validar_departamento(cls, v: str) -> str:
        if v not in DEPARTAMENTOS:
            raise ValueError(
                f"El departamento debe ser uno de: {', '.join(DEPARTAMENTOS)}"
            )
        return v

    @field_validator("fecha_ingreso")
    @classmethod
    def validar_fecha_ingreso(cls, v: date) -> date:
        if v > date.today():
            raise ValueError("La fecha de ingreso no puede ser futura")
        return v


class EmpleadoSalida(BaseModel):
    """Datos que la API devuelve al consultar o registrar un empleado."""

    id: int
    numero_empleado: Optional[str]
    nombre: str
    correo: str
    puesto: str
    departamento: str
    fecha_ingreso: date
    estado: str
    fecha_baja: Optional[date]
    creado_en: datetime

    model_config = {"from_attributes": True}


class EmpleadoListaSalida(BaseModel):
    """Respuesta del listado de empleados, con lista y mensaje opcional."""

    empleados: list[EmpleadoSalida]
    mensaje: str = ""
