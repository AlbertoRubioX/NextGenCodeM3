import React, { useEffect, useState } from "react";
import FormularioEmpleado from "./components/FormularioEmpleado.jsx";
import TablaEmpleados from "./components/TablaEmpleados.jsx";
import { obtenerEmpleados } from "./api.js";

/**
 * Componente raíz de la aplicación de gestión de empleados.
 * Muestra el formulario de alta y la tabla de empleados en la misma página.
 */
export default function App() {
  const [empleados, setEmpleados] = useState([]);

  // Carga inicial de empleados
  useEffect(() => {
    cargarEmpleados();
  }, []);

  async function cargarEmpleados() {
    try {
      const lista = await obtenerEmpleados();
      setEmpleados(lista);
    } catch {
      // Si el backend no está disponible, se muestra la tabla vacía
    }
  }

  function handleEmpleadoCreado(nuevoEmpleado) {
    setEmpleados((anterior) => [...anterior, nuevoEmpleado]);
  }

  return (
    <div style={{ maxWidth: "1000px", margin: "0 auto", padding: "1rem" }}>
      <h1>Gestión de Empleados</h1>
      <FormularioEmpleado onEmpleadoCreado={handleEmpleadoCreado} />
      <h2>Directorio de Empleados</h2>
      <TablaEmpleados empleados={empleados} />
    </div>
  );
}
