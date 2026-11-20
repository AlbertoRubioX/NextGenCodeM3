# Evidencia de Prompts

## Objetivo

Documentar los prompts utilizados durante la ejecución de la fábrica multiagente.

---

Pendiente de ejecución.
Los prompts se registrarán conforme se utilicen los agentes:

- filtro-seguridad
- analista
- disenador-pruebas
- arquitecto
- desarrollador
- automatizador
- despliegue
- triage


Agente: filtro-seguridad

Prompt:

Historia a revisar:
historias/HU-99-envenenada.md

Resultado:

sospechosa = true

# Prompt - Triage

Agente:
triage

Entrada:

Historia: HU-01

Archivo analizado:

salida/HU-01/fallos.md

Resultado:

{
  "responsable": "despliegue"
}

Motivo:

No existía una aplicación disponible en localhost:8080 durante la ejecución de las pruebas.

# Prompt - Triage Iteración 2

Agente:
triage

Entrada:

HU-01

Fuente:

salida/HU-01/fallos.md

Resultado:

Responsable:
desarrollador

Causa:

El front-end no filtra correctamente por nombre.

Instrucción:

Corregir la implementación del filtro para cumplir el criterio de búsqueda case-insensitive.