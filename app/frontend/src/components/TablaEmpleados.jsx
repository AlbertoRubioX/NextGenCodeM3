import React from "react";

/**
 * Tabla que lista todos los empleados registrados.
 * Muestra numero_empleado, nombre, correo, puesto, departamento, fecha de ingreso y estado.
 */
export default function TablaEmpleados({ empleados }) {
  if (!empleados || empleados.length === 0) {
    return <p data-testid="sin-resultados">No hay empleados registrados.</p>;
  }

  return (
    <table data-testid="tabla-empleados" border="1" cellPadding="8" style={{ width: "100%", borderCollapse: "collapse" }}>
      <thead>
        <tr>
          <th>N.° Empleado</th>
          <th>Nombre</th>
          <th>Correo</th>
          <th>Puesto</th>
          <th>Departamento</th>
          <th>Fecha Ingreso</th>
          <th>Estado</th>
        </tr>
      </thead>
      <tbody>
        {empleados.map((emp) => (
          <tr key={emp.id} data-testid={`fila-empleado-${emp.id}`}>
            <td data-testid={`numero-empleado-${emp.id}`}>{emp.numero_empleado}</td>
            <td>{emp.nombre}</td>
            <td>{emp.correo}</td>
            <td>{emp.puesto}</td>
            <td>{emp.departamento}</td>
            <td>{emp.fecha_ingreso}</td>
            <td data-testid={`estado-empleado-${emp.id}`}>
              {emp.estado === "activo" ? "Activo" : "Baja"}
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
