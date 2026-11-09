# Reporte HU-01 · Registrar empleado

**Estado:** LISTA
**Ciclos de corrección:** 1

## Bitácora

| Paso | Resultado |
|------|-----------|
| 0 · Filtro de seguridad | OK — `sospechosa: false` |
| 1 · Analista | 5 escenarios en `criterios.feature` |
| 2 · Compuerta criterios | válido |
| 3 · Preguntas abiertas | 3 preguntas — aprobado por adelantado |
| 4 · Diseñador de pruebas | 6 casos de prueba — válido |
| 5 · Plan y aprobación | `plan.md` generado — aprobado por adelantado |
| 6 · Desarrollador | app implementada (backend FastAPI + frontend React) |
| 7 · Verificación app | OK (corrección: `npm.cmd` en `verificacion/app.py`) |
| 8 · Despliegue + automatizador | OK en paralelo |
| 9 · Verificación despliegue + pruebas | OK |
| 10 · E2E (intento 1) | FALLA — 1 test: CP-05 sin nombre de campo en 422 |
| 11 · Triage ciclo 1 | responsable: desarrollador |
| 11 · Corrección desarrollador | `main.py`: manejador de errores devuelve "El campo {campo} es obligatorio" |
| 11 · Redespliegue | OK (corrección: encoding utf-8 en `verificacion/comun.py`) |
| 10 · E2E (intento 2) | 6/6 ✅ LISTA |

## Correcciones de infraestructura aplicadas

- `verificacion/app.py`: `"npm"` → `"npm.cmd"` en Windows (subprocess no encontraba npm)
- `verificacion/comun.py`: añadido `encoding="utf-8", errors="replace"` y guarda nulos de stdout/stderr (Docker emitía bytes fuera del rango cp1252)

## Resultado final

6 tests pasaron · 0 fallaron · 1 advertencia (Playwright)
