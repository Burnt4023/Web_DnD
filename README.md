# B&B: Gestión de Campañas de D&D Homebrew

## Descripción
Este proyecto tiene como objetivo crear una página web para gestionar las fichas de personajes de **Dungeons & Dragons (D&D)**. Los usuarios pueden crear, modificar y almacenar las fichas de sus personajes y consultar todos los datos que el DM añada a la Wiki.

## Tecnologías Utilizadas
- **Flask**: Framework para el backend.
- **HTML/CSS**: Para la estructura y el diseño de la interfaz de usuario.
- **JavaScript**: Para la interacción dinámica en la página.
- **JSON**: Para almacenar las fichas de los personajes.
- **SQLite**: Para gestionar la persistencia de datos.

## Instalación

### Instrucciones de Instalación
1. Clona este repositorio:
    ```bash
    git clone https://github.com/Burnt4023/Web_DnD.git
    cd Web_DnD
    ```

2. Instala las dependencias necesarias:
   ```
    Flask
    Bcrypt
   ```
4. Inicia la aplicación:
    ```bash
    python server.py
    ```

5. Abre tu navegador y ve a `http://127.0.0.1:5000` para ver la aplicación en funcionamiento.

## Funcionalidades

### Creación de Fichas
Los usuarios pueden crear nuevas fichas de personajes con los siguientes campos (entre otros):
- **Nombre del personaje**
- **Nivel**
- **Clase**
- **Alineamiento**
- **Talento**
- **Magia**
- **Vida, Mana y Resistencia** (Homebrew)
- **Habilidades**: Lista de habilidades del personaje.
- **Hechizos**: Lista de hechizos disponibles para el personaje.
- **Objetos**: Lista de objetos y equipo del personaje.

El proyecto es código abierto, de modo que los campos de las fichas pueden modificarse a gusto para ajustarlos a cualquier campaña.
### Wiki
Los usuarios podrán acceder a una wiki rellenada por el DM con información de la campaña como, por ejemplo, NPCs, lugares, eventos, etc.
