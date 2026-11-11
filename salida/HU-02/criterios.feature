# language: es

Característica: Consultar el directorio de empleados
  Como persona del área de Recursos Humanos
  quiero ver el directorio de empleados, buscarlos por nombre o correo y filtrarlos por departamento
  para encontrar rápido a una persona

  Escenario: Listar todos los empleados del directorio
    Dado que existen al menos los siguientes empleados registrados:
      | numero_empleado | nombre          | puesto              | departamento | estado |
      | EMP-0001        | Ana López       | Analista de Datos   | Tecnología   | activo |
      | EMP-0002        | Pedro García    | Ejecutivo de Ventas | Ventas       | baja   |
    Cuando envío una petición GET a "/empleados"
    Entonces la respuesta tiene código HTTP 200
    Y el cuerpo de la respuesta es una lista que incluye a "Ana López" con numero_empleado "EMP-0001", puesto "Analista de Datos", departamento "Tecnología" y estado "activo"
    Y el cuerpo de la respuesta incluye a "Pedro García" con estado "baja"

  Escenario: Buscar empleado por nombre sin distinguir mayúsculas
    Dado que existe un empleado con nombre "Ana López" en el sistema
    Cuando envío una petición GET a "/empleados?q=ana+lópez"
    Entonces la respuesta tiene código HTTP 200
    Y el cuerpo de la respuesta contiene exactamente 1 empleado con nombre "Ana López"

  Escenario: Buscar empleado por correo en mayúsculas
    Dado que existe un empleado con correo "ana.lopez@empresa.com" en el sistema
    Cuando envío una petición GET a "/empleados?q=ANA.LOPEZ@EMPRESA.COM"
    Entonces la respuesta tiene código HTTP 200
    Y el cuerpo de la respuesta contiene exactamente 1 empleado con correo "ana.lopez@empresa.com"

  Escenario: Filtrar empleados por departamento
    Dado que existen empleados en el departamento "Finanzas" y empleados en el departamento "Ventas"
    Cuando envío una petición GET a "/empleados?departamento=Finanzas"
    Entonces la respuesta tiene código HTTP 200
    Y todos los empleados del cuerpo de la respuesta tienen departamento "Finanzas"
    Y ningún empleado del cuerpo de la respuesta tiene departamento "Ventas"

  Escenario: Búsqueda sin resultados muestra mensaje informativo
    Dado que ningún empleado tiene nombre ni correo que contenga "zzznoencontrado"
    Cuando envío una petición GET a "/empleados?q=zzznoencontrado"
    Entonces la respuesta tiene código HTTP 200
    Y el cuerpo de la respuesta es una lista vacía
    Y la respuesta incluye un mensaje indicando que no se encontraron resultados

  Escenario: Filtro por departamento sin resultados muestra mensaje informativo
    Dado que ningún empleado pertenece al departamento "Operaciones"
    Cuando envío una petición GET a "/empleados?departamento=Operaciones"
    Entonces la respuesta tiene código HTTP 200
    Y el cuerpo de la respuesta es una lista vacía
    Y la respuesta incluye un mensaje indicando que no se encontraron resultados

  Escenario: El directorio muestra empleados dados de baja
    Dado que existe un empleado con nombre "Pedro García" cuyo estado es "baja"
    Cuando envío una petición GET a "/empleados"
    Entonces la respuesta tiene código HTTP 200
    Y el cuerpo de la respuesta incluye a "Pedro García" con estado "baja"

# Preguntas abiertas
# 1. ¿La búsqueda por nombre es por coincidencia parcial (contiene) o solo por coincidencia exacta?
#    La historia dice "buscarlos por nombre", pero no especifica si "Ana" debe encontrar "Ana López".
# 2. ¿Se pueden combinar búsqueda de texto y filtro por departamento en la misma petición
#    (p. ej. /empleados?q=ana&departamento=Tecnología)? La historia no lo menciona explícitamente.
# 3. ¿La pantalla muestra el mensaje "sin resultados" como texto en la tabla o como alerta aparte?
#    Impacta cómo se verifica desde la interfaz.
# 4. ¿El directorio pagina los resultados? Si hay límite por página, falta la regla de paginación.
