function abrirPopup() {
    const overlay = document.querySelector('.popup-overlay');
    const popup = document.querySelector('.popup');
    overlay.classList.add('active');
    popup.classList.add('active');
}

function cerrarPopup() {
    const overlay = document.querySelector('.popup-overlay');
    const popup = document.querySelector('.popup');
    overlay.classList.remove('active');
    popup.classList.remove('active');
}

async function crearFicha() {
    const nombreFicha = document.querySelector('#nombreFicha').value;

    if (!nombreFicha.trim()) {
        alert('El nombre de la ficha no puede estar vacío.');
        return;
    }

    // JSON con los valores iniciales de la ficha
    const fichaInicial = {
        nombre: nombreFicha,
        nivel: 1,
        clase: 'Sin clase',
        magia: 'Ninguna',
        talento: 'Ninguno',
        alineamiento: 'Neutral',
        vida: { actual: 10, maximo: 10 },
        mana: { actual: 10, maximo: 10 },
        stamina: { actual: 10, maximo: 10 },
        sobrecarga: 0,
        velocidad: 30,
        armadura: 10,
        iniciativa: 0,
        historia: 'No',
        foto : "",
        notas : "",
        Proficiencias: [
            15,15,15,
            15,15,15,
            15,15,15,
        ],
        estadisticas: [
            0,0,0,
            0,0,0,
            0,0,0
        ],
        habilidades: [],
        estados: [],
        objetos: [],
        equipamiento: [],
        dinero: [0, 0, 0, 0] //[cobre, plata, oro, platino]
    };

    // Enviar solicitud AJAX para crear la ficha con contenido inicial
    const response = await fetch('/fichas/crear', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ nombre_ficha: nombreFicha, contenido: fichaInicial }),
    });

    const data = await response.json();

    if (data.success) {
        alert('Ficha creada exitosamente.');
        location.reload(); // Recargar la página para mostrar la nueva ficha
    } else {
        alert('Error al crear la ficha: ' + data.error);
    }

    cerrarPopup();
}

// Cerrar popup al hacer clic fuera de él
document.addEventListener('click', (event) => {
    const overlay = document.querySelector('.popup-overlay');
    const popup = document.querySelector('.popup');
    if (event.target === overlay) {
        overlay.classList.remove('active');
        popup.classList.remove('active');
    }
});