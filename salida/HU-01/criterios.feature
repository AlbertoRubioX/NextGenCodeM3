# language: es

Característica: Registrar empleado
  Como persona del área de Recursos Humanos
  quiero registrar a un empleado con su nombre, correo corporativo, puesto, departamento y fecha de ingreso
  para darlo de alta en la empresa

  Escenario: Registro exitoso de un empleado nuevo
    Dado que ningún empleado con correo "ana.lopez@empresa.com" existe en el sistema
    Cuando envío una petición POST a "/empleados" con los datos:
      | campo         | valor                 |
      | nombre        | Ana López             |
      | correo        | ana.lopez@empresa.com |
      | puesto        | Analista de Datos     |
      | departamento  | Tecnología            |
      | fecha_ingreso | 2026-11-08            |
    Entonces la respuesta tiene código HTTP 201
    Y el cuerpo de la respuesta incluye un campo "numero_empleado" con formato "EMP-NNNN"
    Y el cuerpo de la respuesta incluye el campo "numero_empleado" con el número asignado
    Y el campo "estado" en la respuesta es "activo"
    Y el campo "correo" en la respuesta es "ana.lopez@empresa.com" en minúsculas

  Escenario: Rechazo por correo duplicado sin importar mayúsculas
    Dado que ya existe un empleado con correo "pedro.garcia@empresa.com" en el sistema
    Cuando envío una petición POST a "/empleados" con los datos:
      | campo         | valor                    |
      | nombre        | Pedro García             |
      | correo        | PEDRO.GARCIA@empresa.com |
      | puesto        | Ejecutivo de Ventas      |
      | departamento  | Ventas                   |
      | fecha_ingreso | 2026-11-08               |
    Entonces la respuesta tiene código HTTP 409
    Y el cuerpo de la respuesta incluye el mensaje "El correo ya está registrado"

  Escenario: Rechazo por correo con dominio no corporativo
    Dado que ningún empleado con correo "maria.ruiz@gmail.com" existe en el sistema
    Cuando envío una petición POST a "/empleados" con los datos:
      | campo         | valor                |
      | nombre        | María Ruiz           |
      | correo        | maria.ruiz@gmail.com |
      | puesto        | Contadora            |
      | departamento  | Finanzas             |
      | fecha_ingreso | 2026-11-08           |
    Entonces la respuesta tiene código HTTP 422
    Y el cuerpo de la respuesta incluye el mensaje "Usa el correo corporativo @empresa.com"

  Escenario: Rechazo por campo obligatorio ausente
    Dado que quiero registrar un empleado sin indicar el puesto
    Cuando envío una petición POST a "/empleados" con los datos:
      | campo         | valor                   |
      | nombre        | Luis Torres             |
      | correo        | luis.torres@empresa.com |
      | departamento  | Operaciones             |
      | fecha_ingreso | 2026-11-08              |
    Entonces la respuesta tiene código HTTP 422
    Y el cuerpo de la respuesta indica que el campo "puesto" debe corregirse

  Escenario: Rechazo por fecha de ingreso futura
    Dado que ningún empleado con correo "carla.nunez@empresa.com" existe en el sistema
    Cuando envío una petición POST a "/empleados" con los datos:
      | campo         | valor                   |
      | nombre        | Carla Nuñez             |
      | correo        | carla.nunez@empresa.com |
      | puesto        | Gerente de Operaciones  |
      | departamento  | Operaciones             |
      | fecha_ingreso | 2027-01-01              |
    Entonces la respuesta tiene código HTTP 422
    Y el cuerpo de la respuesta incluye el mensaje "La fecha de ingreso no puede ser futura"

# Preguntas abiertas
# 1. ¿El mensaje de confirmación con el número asignado se muestra en un modal,
#    en la misma página o redirige a la ficha del empleado recién creado?
#    La historia dice "quiero ver un mensaje de confirmación", pero no especifica la pantalla destino.
# 2. ¿El formato EMP-NNNN siempre tiene exactamente 4 dígitos (EMP-0001),
#    o puede crecer a más dígitos cuando supere 9999 empleados (EMP-10000)?
# 3. ¿Qué código HTTP y mensaje devuelve la API cuando el departamento enviado
#    no pertenece a la lista permitida (Tecnología, Ventas, Finanzas, Recursos Humanos, Operaciones)?
#    La regla 3 dice 422, pero no especifica el texto del mensaje para este campo concreto.
