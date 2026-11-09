import React, { useEffect, useState } from "react";
import { crearEmpleado, obtenerDepartamentos } from "../api.js";

/**
 * Formulario de alta de empleados.
 * Al guardar exitosamente llama a onEmpleadoCreado con el empleado devuelto por la API.
 */
export default function FormularioEmpleado({ onEmpleadoCreado }) {
  const [departamentos, setDepartamentos] = useState([]);
  const [form, setForm] = useState({
    nombre: "",
    correo: "",
    puesto: "",
    departamento: "",
    fecha_ingreso: "",
  });
  const [mensajeExito, setMensajeExito] = useState("");
  const [mensajeError, setMensajeError] = useState("");
  const [enviando, setEnviando] = useState(false);

  useEffect(() => {
    obtenerDepartamentos()
      .then(setDepartamentos)
      .catch(() => setDepartamentos([]));
  }, []);

  function handleChange(e) {
    setForm({ ...form, [e.target.name]: e.target.value });
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setMensajeExito("");
    setMensajeError("");
    setEnviando(true);

    try {
      const empleado = await crearEmpleado(form);
      setMensajeExito(
        `Empleado registrado con éxito. Número asignado: ${empleado.numero_empleado}`
      );
      setForm({
        nombre: "",
        correo: "",
        puesto: "",
        departamento: "",
        fecha_ingreso: "",
      });
      if (onEmpleadoCreado) {
        onEmpleadoCreado(empleado);
      }
    } catch (error) {
      setMensajeError(error.message || "Ocurrió un error al registrar el empleado");
    } finally {
      setEnviando(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} style={{ marginBottom: "2rem" }}>
      <h2>Registrar Empleado</h2>

      <div>
        <label htmlFor="nombre">Nombre</label>
        <input
          id="nombre"
          name="nombre"
          type="text"
          value={form.nombre}
          onChange={handleChange}
          data-testid="empleado-nombre"
          required
        />
      </div>

      <div>
        <label htmlFor="correo">Correo corporativo</label>
        <input
          id="correo"
          name="correo"
          type="email"
          value={form.correo}
          onChange={handleChange}
          data-testid="empleado-correo"
          required
        />
      </div>

      <div>
        <label htmlFor="puesto">Puesto</label>
        <input
          id="puesto"
          name="puesto"
          type="text"
          value={form.puesto}
          onChange={handleChange}
          data-testid="empleado-puesto"
          required
        />
      </div>

      <div>
        <label htmlFor="departamento">Departamento</label>
        <select
          id="departamento"
          name="departamento"
          value={form.departamento}
          onChange={handleChange}
          data-testid="empleado-departamento"
          required
        >
          <option value="">Selecciona un departamento</option>
          {departamentos.map((dep) => (
            <option key={dep} value={dep}>
              {dep}
            </option>
          ))}
        </select>
      </div>

      <div>
        <label htmlFor="fecha_ingreso">Fecha de ingreso</label>
        <input
          id="fecha_ingreso"
          name="fecha_ingreso"
          type="date"
          value={form.fecha_ingreso}
          onChange={handleChange}
          data-testid="empleado-fecha-ingreso"
          required
        />
      </div>

      <button type="submit" data-testid="empleado-guardar" disabled={enviando}>
        {enviando ? "Guardando..." : "Guardar"}
      </button>

      {mensajeExito && (
        <p data-testid="mensaje-exito" style={{ color: "green" }}>
          {mensajeExito}
        </p>
      )}

      {mensajeError && (
        <p data-testid="mensaje-error" style={{ color: "red" }}>
          {mensajeError}
        </p>
      )}
    </form>
  );
}
