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
        resistencia: { actual: 10, maximo: 10 },
        sobrecarga: 0,
        velocidad: 30,
        armadura: 10,
        iniciativa: 0,
        historia: 'No',
        tiradas: { exito: 0, fallo: 0 },
        destrezas: {
            mineria: 0, herreria: 0, costura: 0, carpinteria: 0,
            arcano: 0, supervivencia: 0, pesca: 0, alquimia: 0,
            cocina: 0, medicina: 0, sigilo: 0, arco: 0,
            espada: 0, bloqueo: 0, engaño: 0, percepcion: 0
        },
        estadisticas: {
            fuerza: 0, resistencia: 0, agilidad: 0,
            poder: 0, control: 0, capacidad: 0,
            carisma: 0, inteligencia: 0, sabiduria: 0
        },
        habilidades: [],
        hechizos: [],
        objetos: [],
        equipamiento: [],
        dinero: [0, 0, 0, 0] // Formato: [cobre, plata, oro, platino]
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