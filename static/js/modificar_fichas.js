function agregarHabilidad() {
    const lista = document.getElementById('lista-habilidades');
    const select = document.getElementById('habilidades-disponibles');
    const habilidadSeleccionada = select.value;

    if (habilidadSeleccionada) {
        const div = document.createElement('div');
        div.innerHTML = `
            <input type="text" name="habilidades[]" value="${habilidadSeleccionada}" readonly required>
            <button type="button" onclick="eliminarHabilidad(this)">Eliminar</button>
        `;
        lista.appendChild(div);

        // Resetear la selección
        select.value = "";
    } else {
        alert("Selecciona una habilidad válida.");
    }
}

function eliminarHabilidad(button) {
    button.parentElement.remove();
}

function agregarHechizo() {
    const lista = document.getElementById('lista-hechizos');
    const select = document.getElementById('hechizos-disponibles');
    const hechizoSeleccionado = select.value;

    if (hechizoSeleccionado) {
        const div = document.createElement('div');
        div.innerHTML = `
            <input type="text" name="hechizos[]" value="${hechizoSeleccionado}" readonly required>
            <button type="button" onclick="eliminarHechizo(this)">Eliminar</button>
        `;
        lista.appendChild(div);

        // Resetear la selección
        select.value = "";
    } else {
        alert("Selecciona un hechizo válido.");
    }
}

function eliminarHechizo(button) {
    button.parentElement.remove();
}

function agregarEquipo() {
    const lista = document.getElementById('lista-equipo');
    const select = document.getElementById('equipo-disponible');
    const equipoSeleccionado = select.value;

    if (equipoSeleccionado) {
        const div = document.createElement('div');
        div.innerHTML = `
            <input type="text" name="equipo[]" value="${equipoSeleccionado}" readonly required>
            <button type="button" onclick="eliminarEquipo(this)">Eliminar</button>
        `;
        lista.appendChild(div);

        // Resetear la selección
        select.value = "";
    } else {
        alert("Selecciona un objeto válido.");
    }
}

function eliminarEquipo(button) {
    button.parentElement.remove();
}

function agregarObjeto() {
    const lista = document.getElementById('lista-objetos');
    const select = document.getElementById('objetos-disponibles');
    const objetoSeleccionado = select.value;

    if (objetoSeleccionado) {
        const div = document.createElement('div');
        div.innerHTML = `
            <input type="text" name="objetos[]" value="${objetoSeleccionado}" readonly required>
            <button type="button" onclick="eliminarObjeto(this)">Eliminar</button>
        `;
        lista.appendChild(div);

        // Resetear la selección
        select.value = "";
    } else {
        alert("Selecciona un objeto válido.");
    }
}

function eliminarObjeto(button) {
    button.parentElement.remove();
}

function agregarInventario() {
    const lista = document.getElementById('lista-inventario');
    const select = document.getElementById('inventario-disponible');
    const inventarioSeleccionado = select.value;

    if (inventarioSeleccionado) {
        const div = document.createElement('div');
        div.innerHTML = `
            <input type="text" name="objetos[]" value="${inventarioSeleccionado}" readonly required>
            <button type="button" onclick="eliminarInventario(this)">Eliminar</button>
        `;
        lista.appendChild(div);

        // Resetear la selección
        select.value = "";
    } else {
        alert("Selecciona un objeto válido.");
    }
}

function eliminarInventario(button) {
    button.parentElement.remove();
}
