import React, { useState } from "react";
import { darDeBaja } from "../api.js";

/**
 * Tabla que lista todos los empleados registrados.
 * Muestra numero_empleado, nombre, correo, puesto, departamento, fecha de ingreso, estado y acciones.
 * Acepta la prop `mensaje` para mostrar el texto de "sin resultados" cuando la lista está vacía.
 * Acepta la prop `onBaja` para notificar al padre cuando un empleado es dado de baja.
 */
export default function TablaEmpleados({ empleados, mensaje, onBaja }) {
  // id del empleado cuya confirmación de baja está abierta, o null
  const [confirmandoId, setConfirmandoId] = useState(null);
  const [fechaBajaInput, setFechaBajaInput] = useState("");
  const [errorBaja, setErrorBaja] = useState("");
  const [procesando, setProcesando] = useState(false);

  function abrirConfirmacion(id) {
    setConfirmandoId(id);
    setFechaBajaInput("");
    setErrorBaja("");
  }

  function cancelarConfirmacion() {
    setConfirmandoId(null);
    setFechaBajaInput("");
    setErrorBaja("");
  }

  async function confirmarBaja() {
    if (!confirmandoId) return;
    setProcesando(true);
    setErrorBaja("");
    try {
      await darDeBaja(confirmandoId);
      setConfirmandoId(null);
      setFechaBajaInput("");
      if (onBaja) onBaja();
    } catch (err) {
      setErrorBaja(err.message || "Error al dar de baja");
    } finally {
      setProcesando(false);
    }
  }

  return (
    <>
      {/* Panel de confirmación de baja */}
      {confirmandoId !== null && (
        <div style={{ border: "1px solid #ccc", padding: "1rem", marginBottom: "1rem", background: "#fff8e1" }}>
          <p>¿Confirmar baja del empleado?</p>
          <div>
            <label htmlFor="fecha-baja-input">Fecha de baja</label>
            <input
              id="fecha-baja-input"
              data-testid="empleado-fecha-baja"
              type="date"
              value={fechaBajaInput}
              onChange={(e) => setFechaBajaInput(e.target.value)}
              style={{ marginLeft: "0.5rem" }}
            />
          </div>
          {errorBaja && (
            <p style={{ color: "red" }}>{errorBaja}</p>
          )}
          <button
            data-testid="confirmar-baja"
            onClick={confirmarBaja}
            disabled={procesando}
            style={{ marginTop: "0.5rem", marginRight: "0.5rem" }}
          >
            {procesando ? "Procesando..." : "Confirmar baja"}
          </button>
          <button onClick={cancelarConfirmacion} disabled={procesando}>
            Cancelar
          </button>
        </div>
      )}

      <table
        data-testid="tabla-empleados"
        border="1"
        cellPadding="8"
        style={{ width: "100%", borderCollapse: "collapse" }}
      >
        <thead>
          <tr>
            <th>N.° Empleado</th>
            <th>Nombre</th>
            <th>Correo</th>
            <th>Puesto</th>
            <th>Departamento</th>
            <th>Fecha Ingreso</th>
            <th>Estado</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          {empleados && empleados.map((emp) => (
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
              <td>
                {emp.estado === "activo" && (
                  <button
                    data-testid={`baja-empleado-${emp.id}`}
                    onClick={() => abrirConfirmacion(emp.id)}
                  >
                    Dar de baja
                  </button>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      {(!empleados || empleados.length === 0) && mensaje && (
        <p data-testid="sin-resultados">{mensaje}</p>
      )}
    </>
  );
}
