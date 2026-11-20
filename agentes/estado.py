from typing import TypedDict, List


class EstadoProyecto(TypedDict):
    requerimiento: str

    especificacion: str

    plan: str

    codigo_generado: str

    pruebas_generadas: str

    revision: str

    alertas_seguridad: List[str]

    aprobado: bool
