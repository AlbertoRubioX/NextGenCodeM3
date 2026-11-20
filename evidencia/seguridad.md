# Evidencias de Seguridad

## Objetivo

Implementar controles de seguridad independientes del modelo para proteger el flujo multiagente frente a prompt injection, acceso indebido a recursos y fuga de información.

---

# Prompt Hardening

Implementado mediante:

- hooks/seguridad.py
- filtro-seguridad.md

Descripción:

Las historias de usuario son consideradas contenido NO confiable.

El agente filtro-seguridad analiza la historia antes de que cualquier otro agente la procese y determina si contiene instrucciones dirigidas a manipular el comportamiento del sistema.

Ejemplo:

- Ignorar instrucciones previas
- Leer secretos
- Mostrar variables de entorno
- Exponer archivos internos

Resultado:

Se genera veredicto.json con el resultado del análisis.

---

# Input Validation

Implementado mediante:

- hooks/seguridad.py
- validadores/

Controles:

## Lectura confinada

Se valida que todas las rutas se mantengan dentro del directorio del proyecto.

Ejemplo:

```python
if not destino.is_relative_to(RAIZ):