import React, { useEffect, useRef, useState } from "react";
import FormularioEmpleado from "./components/FormularioEmpleado.jsx";
import TablaEmpleados from "./components/TablaEmpleados.jsx";
import FiltrosDirectorio from "./components/FiltrosDirectorio.jsx";
import { obtenerEmpleados } from "./api.js";

/**
 * Componente raíz de la aplicación de gestión de empleados.
 * Muestra el formulario de alta, los filtros del directorio y la tabla de empleados.
 *
 * Estrategia de filtrado:
 * - Tanto el filtro de texto (q) como el filtro por departamento se envían al backend.
 * - Se aplica un debounce de 300 ms sobre el parámetro q para evitar demasiadas
 *   peticiones mientras el usuario escribe.
 */
export default function App() {
  const [empleados, setEmpleados] = useState([]);
  const [mensaje, setMensaje] = useState("");

  // Filtros actuales tal como los comunica FiltrosDirectorio
  const [filtros, setFiltros] = useState({ q: "", departamento: "" });

  // Referencia al temporizador de debounce del parámetro q
  const temporizadorQ = useRef(null);
  // Filtros que se mandan realmente al backend (q con debounce aplicado)
  const [filtrosEfectivos, setFiltrosEfectivos] = useState({ q: "", departamento: "" });

  // Cuando cambian los filtros efectivos, recarga la lista desde el backend
  useEffect(() => {
    cargarEmpleados(filtrosEfectivos);
  }, [filtrosEfectivos]);

  async function cargarEmpleados(params) {
    try {
      const resultado = await obtenerEmpleados(params);
      setEmpleados(resultado.empleados ?? []);
      setMensaje(resultado.mensaje ?? "");
    } catch {
      setEmpleados([]);
      setMensaje("");
    }
  }

  function handleEmpleadoCreado() {
    // Recarga la lista respetando los filtros activos
    cargarEmpleados(filtrosEfectivos);
  }

  function handleFiltrar(nuevosFiltros) {
    setFiltros(nuevosFiltros);

    // El departamento se envía al backend de inmediato (ya viene con debounce
    // desde FiltrosDirectorio). El parámetro q usa un debounce adicional aquí
    // para no lanzar una petición por cada tecla pulsada.
    if (temporizadorQ.current) clearTimeout(temporizadorQ.current);
    temporizadorQ.current = setTimeout(() => {
      setFiltrosEfectivos(nuevosFiltros);
    }, 300);
  }

  return (
    <div style={{ maxWidth: "1000px", margin: "0 auto", padding: "1rem" }}>
      <h1>Gestión de Empleados</h1>
      <FormularioEmpleado onEmpleadoCreado={handleEmpleadoCreado} />
      <h2>Directorio de Empleados</h2>
      <FiltrosDirectorio onFiltrar={handleFiltrar} />
      <TablaEmpleados
        empleados={empleados}
        mensaje={mensaje}
        onBaja={() => cargarEmpleados(filtrosEfectivos)}
      />
    </div>
  );
}
