function agregarHabilidad() {
    const lista = document.getElementById('lista-habilidades');
    const select = document.getElementById('habilidades-disponibles');
    const habilidadSeleccionada = select.value;

    if (habilidadSeleccionada) {
        const div = document.createElement('div');
        div.innerHTML = `
            <input type="text" name="habilidades[]" value="${habilidadSeleccionada}" readonly required class="w-full p-2 bg-gray-700 rounded-lg">
            <button type="button" onclick="eliminarHabilidad(this)" class="bg-red-500 hover:bg-red-600 px-2 py-1 rounded-lg">Eliminar</button>
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
            <input type="text" name="hechizos[]" value="${hechizoSeleccionado}" readonly required class="w-full p-2 bg-gray-700 rounded-lg">
            <button type="button" onclick="eliminarHechizo(this)" class="bg-red-500 hover:bg-red-600 px-2 py-1 rounded-lg">Eliminar</button>
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
            <input type="text" name="equipo[]" value="${equipoSeleccionado}" readonly required class="w-full p-2 bg-gray-700 rounded-lg">
            <button type="button" onclick="eliminarEquipo(this)" class="bg-red-500 hover:bg-red-600 px-2 py-1 rounded-lg">Eliminar</button>
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
            <input type="text" name="objetos[]" value="${objetoSeleccionado}" readonly required class="w-full p-2 bg-gray-700 rounded-lg">
            <button type="button" onclick="eliminarObjeto(this)" class="bg-red-500 hover:bg-red-600 px-2 py-1 rounded-lg">Eliminar</button>
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
            <input type="text" name="objetos[]" value="${inventarioSeleccionado}" readonly required class="w-full p-2 bg-gray-700 rounded-lg">
            <button type="button" onclick="eliminarInventario(this)" class="bg-red-500 hover:bg-red-600 px-2 py-1 rounded-lg">Eliminar</button>
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

function filtrarHabilidades() {
    const input = document.getElementById("busqueda-habilidad").value.toLowerCase();
    const select = document.getElementById("habilidades-disponibles");
    const options = select.getElementsByTagName("option");

    for (let i = 1; i < options.length; i++) { // Saltar la primera opción (placeholder)
        const habilidad = options[i].textContent.toLowerCase();
        options[i].style.display = habilidad.includes(input) ? "block" : "none";
    }
}
function filtrarHechizos() {
    const input = document.getElementById("busqueda-hechizo").value.toLowerCase();
    const select = document.getElementById("hechizos-disponibles");
    const options = select.getElementsByTagName("option");

    for (let i = 1; i < options.length; i++) { // Saltar la primera opción (placeholder)
        const hechizo = options[i].textContent.toLowerCase();
        options[i].style.display = hechizo.includes(input) ? "block" : "none";
    }
}

function agregarEstado() {
    const lista = document.getElementById('lista-estados');
    const select = document.getElementById('estados-disponibles');
    const estadoSeleccionado = select.value;

    if (estadoSeleccionado) {
        const div = document.createElement('div');
        div.innerHTML = `
            <input type="text" name="estados[]" value="${estadoSeleccionado}" readonly required class="w-full p-2 bg-gray-700 rounded-lg">
            <button type="button" onclick="eliminarEstado(this)" class="bg-red-500 hover:bg-red-600 px-2 py-1 rounded-lg">Eliminar</button>
        `;
        lista.appendChild(div);

        // Resetear la selección
        select.value = "";
    } else {
        alert("Selecciona un estado válido.");
    }
}

function eliminarEstado(button) {
    button.parentElement.remove();
}

function filtrarEstados() {
    const filtro = document.getElementById('busqueda-estado').value.toLowerCase();
    const opciones = document.getElementById('estados-disponibles').getElementsByTagName('option');

    for (let i = 0; i < opciones.length; i++) {
        const option = opciones[i];
        const texto = option.textContent.toLowerCase();
        if (texto.includes(filtro)) {
            option.style.display = "";
        } else {
            option.style.display = "none";
        }
    }
}
