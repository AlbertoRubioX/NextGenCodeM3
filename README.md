# Multi-Agent Software Factory

Proyecto desarrollado para el reto del Módulo 3: Construcción de Sistemas Agénticos.

La solución implementa una fábrica de software multiagente capaz de transformar una historia de usuario en artefactos de especificación, pruebas, plan de implementación, código, despliegue y validación E2E mediante agentes especializados.

---

# Objetivo

Demostrar la construcción de un sistema multiagente con:

- Orquestación mediante supervisor
- Agentes especializados
- Validaciones automáticas
- Seguridad integrada
- Human In The Loop (HITL)
- Flujo E2E de desarrollo

---


# Tecnologías

Python 3.12
FastAPI
React + Vite
SQLite
Pytest
Playwright
Docker
Seguridad
Prompt Hardening
Input Validation
Output Validation
Auditoría
Sandbox de ejecución
---
# Seguridad
Prompt Hardening
Input Validation
Output Validation
Auditoría
Sandbox de ejecución

---
# Evidencias
La documentación del proyecto se encuentra en:
evidencia/
├── prompts.md
├── iteraciones.md
├── seguridad.md
└── reflexion.md

---
# Arquitectura

```text
Historia de Usuario
        ↓
Filtro de Seguridad
        ↓
Analista
        ↓
Diseñador de Pruebas
        ↓
Arquitecto
        ↓
HITL
        ↓
Desarrollador
        ↓
Despliegue + Automatización
        ↓
Pruebas E2E
        ↓
Triage
        ↓
Reporte Final

