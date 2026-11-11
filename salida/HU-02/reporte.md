# Reporte HU-02 · Consultar el directorio de empleados

**Estado:** ESCALAR A UNA PERSONA
**Ciclos de corrección:** 2 (máximo alcanzado) + intervención manual

## Bitácora

| Paso | Resultado |
|------|-----------|
| 0 · Filtro de seguridad | OK — `sospechosa: false` |
| 1 · Analista | 7 escenarios en `criterios.feature` |
| 2 · Compuerta criterios | válido |
| 3 · Preguntas abiertas | 4 preguntas — aprobado por la persona |
| 4 · Diseñador de pruebas | 14 casos de prueba — válido |
| 5 · Plan y aprobación | `plan.md` aprobado por la persona |
| 6 · Desarrollador | app implementada (filtros q/departamento, FiltrosDirectorio.jsx) |
| 7 · Verificación app | OK (fix encoding `__main__.py`) |
| 8 · Despliegue + automatizador | OK en paralelo — 20 tests recolectados |
| 9 · Verificación despliegue + pruebas | OK |
| 10 · E2E intento 1 | FALLA — 5 fallos (PATCH baja 404, filtrado no funciona) |
| 11 · Triage ciclo 1 | responsable: desarrollador |
| 11 · Corrección ciclo 1 | PATCH /baja añadido; filtro client-side en App.jsx |
| 11 · Redespliegue ciclo 1 | OK |
| 10 · E2E intento 2 | FALLA — 4 fallos (Pedro García sigue 'Activo', filtrado no funciona) |
| 11 · Triage ciclo 2 | responsable: desarrollador |
| 11 · Corrección ciclo 2 | siembra de datos iniciales; filtro backend con normalización Unicode |
| 11 · Redespliegue ciclo 2 | OK |
| 10 · E2E intento 3 | FALLA — 4 fallos persistentes |

## Fallos persistentes tras 2 ciclos

```
- test_cp02_listar_empleados_en_tabla[chromium]
  Pedro García aparece como 'Activo' en lugar de 'Baja'

- test_cp04_buscar_por_nombre_case_insensitive[chromium]
  Búsqueda de 'ana lopez' devuelve 19 filas en lugar de 1

- test_cp06_buscar_por_correo_mayusculas[chromium]
  Búsqueda por correo en mayúsculas devuelve 0 filas en lugar de 1

- test_cp14_directorio_muestra_empleados_baja[chromium]
  Pedro García aparece como 'Activo' en lugar de 'Baja'
```

## Análisis probable de la causa raíz

1. **Volumen Docker persistente**: La siembra de datos solo corre si la BD está vacía.
   El volumen `./backend/datos` persiste entre redespliegues con Pedro García en estado
   `activo` creado por tests anteriores. Eliminar el volumen con `docker compose down -v`
   antes de redesplegar permitiría que la siembra cree a Pedro García como `baja`.

2. **Filtrado en frontend**: El debounce de App.jsx puede no estar enviando el parámetro
   `q` al backend en el tiempo que espera Playwright. Revisar si el test necesita esperar
   a la respuesta de red o si el debounce es demasiado largo para los timeouts de Playwright.
