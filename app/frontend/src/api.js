/**
 * Funciones de acceso a la API del backend.
 * Siempre usa rutas relativas para que el proxy de Vite redirija al backend.
 */

/**
 * Registra un nuevo empleado.
 * @param {Object} datos - Campos del empleado.
 * @returns {Promise<Object>} Empleado creado o error con detalle.
 */
export async function crearEmpleado(datos) {
  const respuesta = await fetch("/api/empleados", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(datos),
  });

  const cuerpo = await respuesta.json();

  if (!respuesta.ok) {
    const mensaje =
      typeof cuerpo.detail === "string"
        ? cuerpo.detail
        : Array.isArray(cuerpo.detail)
        ? cuerpo.detail.map((e) => `${e.loc?.slice(-1)[0] ?? ""}: ${e.msg}`).join("; ")
        : "Error desconocido";
    const error = new Error(mensaje);
    error.status = respuesta.status;
    throw error;
  }

  return cuerpo;
}

/**
 * Obtiene la lista de empleados, con filtros opcionales.
 * @param {Object} params - Parámetros de búsqueda: { q, departamento }.
 * @returns {Promise<{ empleados: Array, mensaje: string }>} Resultado con lista y mensaje.
 */
export async function obtenerEmpleados(params = {}) {
  const qs = new URLSearchParams();
  if (params.q) qs.set("q", params.q);
  if (params.departamento) qs.set("departamento", params.departamento);

  const url = qs.toString() ? `/api/empleados?${qs.toString()}` : "/api/empleados";

  const respuesta = await fetch(url);
  if (!respuesta.ok) {
    throw new Error("No se pudo cargar la lista de empleados");
  }
  return respuesta.json();
}

/**
 * Obtiene los departamentos válidos.
 * @returns {Promise<Array<string>>} Lista de departamentos.
 */
export async function obtenerDepartamentos() {
  const respuesta = await fetch("/api/departamentos");
  if (!respuesta.ok) {
    throw new Error("No se pudo cargar la lista de departamentos");
  }
  return respuesta.json();
}

/**
 * Da de baja a un empleado (cambia su estado a 'baja').
 * @param {number} id - Identificador del empleado.
 * @returns {Promise<Object>} Empleado actualizado.
 */
export async function darDeBaja(id) {
  const respuesta = await fetch(`/api/empleados/${id}/baja`, {
    method: "PATCH",
  });

  const cuerpo = await respuesta.json();

  if (!respuesta.ok) {
    const mensaje =
      typeof cuerpo.detail === "string" ? cuerpo.detail : "Error al dar de baja";
    const error = new Error(mensaje);
    error.status = respuesta.status;
    throw error;
  }

  return cuerpo;
}
