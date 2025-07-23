# 📦 Carpeta `partials/` en proyectos Flask

El nombre `partials` se refiere a “fragmentos” o “secciones” reutilizables en las plantillas HTML de un proyecto. En este contexto, son archivos de plantilla parciales que:

- 💡 Representan componentes reutilizables
- 🧽 Ayudan a mantener los templates principales más limpios
- 🔁 Se pueden incluir con `{% include %}` en múltiples vistas

---

## 🧩 ¿Qué suele ir dentro de `partials/`?

### 1. 📣 Mensajes dinámicos
Se usan para mostrar validaciones, errores o alertas de éxito.

**Ejemplos:**
- `mensajes.html`
- `errores_formulario.html`

---

### 2. 🧱 Cabeceras y pies de página
Fragmentos HTML que se repiten en todas las vistas del proyecto.

**Ejemplos:**
- `header.html`
- `footer.html`
- `navbar.html`

---

### 3. 📦 Modales o popups
Cuadros flotantes para confirmar acciones, editar miembros, etc.

**Ejemplos:**
- `popup_confirmacion.html`
- `modal_editar_miembro.html`

---

### 4. 📋 Fragmentos de formularios
Campos que se reutilizan en múltiples contextos, como fechas o teléfonos.

**Ejemplos:**
- `campo_fecha_nacimiento.html`
- `campo_telefono.html`

---

### 5. 🧠 Scripts reutilizables
Lógica en JavaScript que se comparte entre distintas vistas.

**Ejemplos:**
- `script_edad.js`
- `script_validacion_telefono.js`

---

🛠️ Mantener estos bloques separados en `partials/` ayuda a escalar el proyecto, mejorar la lectura del código y facilitar el mantenimiento de las interfaces.
