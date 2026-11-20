# CHANGELOG

Todos los cambios relevantes del proyecto serán documentados en este archivo.


### Agregado

- Implementación de una fábrica de software multiagente.
- Definición del flujo de orquestación mediante supervisor.
- Integración de los agentes:
  - filtro-seguridad
  - analista
  - disenador-pruebas
  - arquitecto
  - desarrollador
  - automatizador
  - despliegue
  - triage
- Implementación de HITL (Human In The Loop) para aprobación del plan de implementación.
- Diseño del estado compartido entre agentes (`agentes/estado.py`).
- Documentación de arquitectura multiagente (`contexto/arquitectura_multiagente.md`).
- Carpeta de evidencias para registrar prompts, iteraciones, seguridad y reflexión.

### Seguridad

- Implementación de prompt hardening.
- Validación de entradas mediante validadores y hooks de seguridad.
- Validación de salidas mediante contratos y compuertas.
- Auditoría de acciones en `auditoria.jsonl`.
- Protección contra acceso a secretos y lectura fuera del proyecto.
- Restricción de herramientas según rol de agente.

### Validación y pruebas

- Integración de verificaciones automáticas para:
  - aplicación
  - despliegue
  - pruebas
  - flujo E2E
- Implementación de análisis de fallos mediante triage.
- Generación automatizada de diagnósticos (`diagnostico.json`).

### Documentación

- Actualización de `CLAUDE.md`.
- Creación de `README.md`.
- Creación de documentación de seguridad.
- Generación de evidencias del proceso de desarrollo multiagente.