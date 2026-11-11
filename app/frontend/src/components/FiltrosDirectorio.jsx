import React, { useEffect, useState } from "react";
import { obtenerDepartamentos } from "../api.js";

/**
 * Barra de filtros del directorio: campo de búsqueda de texto y selector de departamento.
 *
 * Ambos controles notifican de inmediato a través de onFiltrar({ q, departamento }).
 * El debounce se gestiona en el componente padre (App) para centralizar la lógica
 * de cuándo lanzar la petición al backend.
 */
export default function FiltrosDirectorio({ onFiltrar }) {
  const [q, setQ] = useState("");
  const [departamento, setDepartamento] = useState("");
  const [departamentos, setDepartamentos] = useState([]);

  // Cargar departamentos del catálogo al montar
  useEffect(() => {
    obtenerDepartamentos()
      .then(setDepartamentos)
      .catch(() => {});
  }, []);

  function handleQ(e) {
    const valor = e.target.value;
    setQ(valor);
    onFiltrar({ q: valor, departamento });
  }

  function handleDepartamento(e) {
    const valor = e.target.value;
    setDepartamento(valor);
    onFiltrar({ q, departamento: valor });
  }

  return (
    <div style={{ display: "flex", gap: "1rem", marginBottom: "1rem", flexWrap: "wrap" }}>
      <input
        data-testid="buscar-empleados"
        type="text"
        placeholder="Buscar por nombre o correo..."
        value={q}
        onChange={handleQ}
        style={{ flex: "1", minWidth: "200px", padding: "0.4rem" }}
      />
      <select
        data-testid="filtro-departamento"
        value={departamento}
        onChange={handleDepartamento}
        style={{ padding: "0.4rem" }}
      >
        <option value="">Todos los departamentos</option>
        {departamentos.map((dep) => (
          <option key={dep} value={dep}>
            {dep}
          </option>
        ))}
      </select>
    </div>
  );
}
