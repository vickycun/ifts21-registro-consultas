const API = (window.API_BASE_URL || "").replace(/\/$/, "");
const $ = (id) => document.getElementById(id);
const usuario = $("usuario");
const resultado = $("resultado");

async function pedir(ruta, opciones = {}) {
  const respuesta = await fetch(`${API}${ruta}`, opciones);
  if (!respuesta.ok) {
    let detalle = `Error HTTP ${respuesta.status}`;
    try { const cuerpo = await respuesta.json(); detalle = typeof cuerpo.detail === "string" ? cuerpo.detail : detalle; } catch {}
    throw new Error(detalle);
  }
  return respuesta.json();
}

async function cargarUsuarios(apellido = "") {
  try {
    const ruta = apellido ? `/api/usuarios?apellido=${encodeURIComponent(apellido)}` : "/api/usuarios";
    const alumnos = await pedir(ruta);
    usuario.replaceChildren();
    if (!alumnos.length) {
      usuario.add(new Option("Sin alumnos encontrados", ""));
      return;
    }
    for (const a of alumnos) usuario.add(new Option(`${a.nombre} ${a.apellido}`, a.id));
  } catch (error) { resultado.textContent = `No se pudieron cargar los alumnos: ${error.message}`; }
}

function mostrarFecha(valor) { return valor ? new Date(valor.replace(" ", "T")).toLocaleString("es-AR") : ""; }

async function cargarHistorial() {
  const seleccionado = $("filtro").value === "actual" ? usuario.value : "";
  const ruta = seleccionado ? `/api/consultas?usuario_id=${encodeURIComponent(seleccionado)}` : "/api/consultas";
  const contenedor = $("historial");
  contenedor.textContent = "Cargando...";
  try {
    const consultas = await pedir(ruta);
    contenedor.replaceChildren();
    if (!consultas.length) { contenedor.textContent = "Todavía no hay consultas registradas."; return; }
    for (const c of consultas) {
      const articulo = document.createElement("article"); articulo.className = "consulta";
      const titulo = document.createElement("strong"); titulo.textContent = `${c.nombre} ${c.apellido}`;
      const fecha = document.createElement("small"); fecha.textContent = mostrarFecha(c.fecha);
      const descripcion = document.createElement("p"); descripcion.textContent = c.descripcion;
      const estado = document.createElement("span"); estado.className = `estado ${c.estado}`; estado.textContent = c.estado;
      const boton = document.createElement("button"); boton.className = "secundario";
      boton.textContent = c.estado === "pendiente" ? "Marcar resuelta" : "Reabrir";
      boton.addEventListener("click", async () => {
        boton.disabled = true;
        try {
          await pedir(`/api/consultas/${c.id}`, {method:"PATCH", headers:{"Content-Type":"application/json"}, body:JSON.stringify({estado:c.estado === "pendiente" ? "resuelta" : "pendiente"})});
          await cargarHistorial();
        } catch (error) { resultado.textContent = error.message; boton.disabled = false; }
      });
      articulo.append(titulo, fecha, descripcion, estado, boton); contenedor.append(articulo);
    }
  } catch (error) { contenedor.textContent = `No se pudo cargar el historial: ${error.message}`; }
}

$("buscar").addEventListener("click", async () => { await cargarUsuarios($("apellido").value.trim()); if ($("filtro").value === "actual") await cargarHistorial(); });
$("todos").addEventListener("click", async () => { $("apellido").value = ""; await cargarUsuarios(); if ($("filtro").value === "actual") await cargarHistorial(); });
$("actualizar").addEventListener("click", cargarHistorial);
$("filtro").addEventListener("change", cargarHistorial);
usuario.addEventListener("change", () => { if ($("filtro").value === "actual") cargarHistorial(); });
$("form").addEventListener("submit", async (evento) => {
  evento.preventDefault(); resultado.textContent = "Guardando...";
  if (!usuario.value) { resultado.textContent = "Seleccioná un alumno"; return; }
  try {
    await pedir("/api/consultas", {method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify({usuario_id:Number(usuario.value), descripcion:$("descripcion").value.trim()})});
    resultado.textContent = "✓ Consulta registrada correctamente";
    $("descripcion").value = "";
    await cargarHistorial();
  } catch (error) { resultado.textContent = `No se pudo registrar: ${error.message}`; }
});
Promise.all([cargarUsuarios(), cargarHistorial()]);
