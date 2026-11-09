"""
Modelos SQLAlchemy para la gestión de empleados.
"""
import os
from datetime import datetime

from sqlalchemy import create_engine, Integer, String, Date, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

# Ruta a la base de datos
_DIR = os.path.join(os.path.dirname(__file__), "datos")
os.makedirs(_DIR, exist_ok=True)
DATABASE_URL = f"sqlite:///{os.path.join(_DIR, 'empleados.db')}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


class Base(DeclarativeBase):
    pass


class Empleado(Base):
    """Tabla principal de empleados."""

    __tablename__ = "empleados"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    numero_empleado: Mapped[str] = mapped_column(String(10), unique=True, nullable=True)
    nombre: Mapped[str] = mapped_column(String(80), nullable=False)
    correo: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    puesto: Mapped[str] = mapped_column(String(60), nullable=False)
    departamento: Mapped[str] = mapped_column(String(40), nullable=False)
    fecha_ingreso: Mapped[datetime] = mapped_column(Date, nullable=False)
    estado: Mapped[str] = mapped_column(String(10), nullable=False, default="activo")
    fecha_baja: Mapped[datetime | None] = mapped_column(Date, nullable=True)
    creado_en: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )


def crear_tablas() -> None:
    """Crea las tablas si no existen."""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Generador de sesiones de base de datos para FastAPI."""
    with Session(engine) as db:
        yield db
