// Obtener elementos del DOM para login
var loginModal = document.getElementById("loginModal");
var loginBtn = document.getElementById("loginBtn");
var closeLoginBtn = document.getElementsByClassName("close")[0];

// Obtener elementos del DOM para registro
var registerModal = document.getElementById("registerModal");
var registerBtn = document.getElementById("registerBtn");
var closeRegisterBtn = document.getElementsByClassName("close")[1];

// Abrir el modal de login
loginBtn.onclick = function() {
    loginModal.style.display = "block";
}

// Abrir el modal de registro
registerBtn.onclick = function() {
    registerModal.style.display = "block";
}

// Cerrar el modal de login al hacer clic en "x"
closeLoginBtn.onclick = function() {
    loginModal.style.display = "none";
}

// Cerrar el modal de registro al hacer clic en "x"
closeRegisterBtn.onclick = function() {
    registerModal.style.display = "none";
}

// Cerrar el modal al hacer clic fuera de él
window.onclick = function(event) {
    if (event.target == loginModal) {
        loginModal.style.display = "none";
    } else if (event.target == registerModal) {
        registerModal.style.display = "none";
    }
}

// Manejo de formularios (agrega esta parte para AJAX)
const registerForm = document.getElementById('registerForm'); // Corrected id
const loginForm = document.getElementById('loginForm');

registerForm.addEventListener('submit', (event) => {
    event.preventDefault(); // Prevent default form submission
    const username = document.getElementById('new_username').value;
    const password = document.getElementById('new_password').value;

    fetch('/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password })
    })
    .then(response => {
        if (response.ok) {
            // Registro exitoso
            alert('User registered successfully!');
            // You could also close the modal here
        } else {
            // Handle errors
            response.json().then(data => {
                alert(data.error);
            });
        }
    });
});

loginForm.addEventListener('submit', (event) => {
    event.preventDefault(); // Prevent default form submission
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password })
    })
    .then(response => {
        if (response.ok) {
            // Login exitoso
            alert('Login successful!');
            // Redirect to principal.html (You might need to update this based on your setup)
            window.location.href = '/principal.html';
        } else {
            // Handle errors
            response.json().then(data => {
                alert(data.error);
            });
        }
    });
});