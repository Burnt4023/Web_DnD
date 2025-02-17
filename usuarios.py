import sqlite3
import bcrypt

# Crear la tabla 'usuarios'
def crear_tabla_usuarios():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS usuarios (
            username TEXT PRIMARY KEY,
            contraseña TEXT NOT NULL,
            admin Boolean NOT NULL
        )
    ''')
    conn.commit()
    conn.close()



# Obtener un usuario por nombre
def obtener_usuario_por_nombre(username):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM usuarios WHERE username = ?', (username,))
    usuario = cursor.fetchone()

    conn.close()
    return usuario

# Validar si las credenciales del usuario son correctas
def validar_usuario(username, contraseña):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT contraseña FROM usuarios WHERE username = ?', (username,))
    result = cursor.fetchone()

    conn.close()

    if result:
        # Verificar si la contraseña coincide con el hash almacenado
        if bcrypt.checkpw(contraseña.encode('utf-8'), result[0]):
            return True
    return False

# Función para registrar un nuevo usuario con contraseñas encriptadas
def registrar_usuario(username, contraseña):
    # Verificar que el nombre de usuario no esté vacío o en uso
    if obtener_usuario_por_nombre(username):
        print(f"El usuario '{username}' ya está en uso.")
        return

    # Generar el hash de la contraseña
    hashed_password = bcrypt.hashpw(contraseña.encode('utf-8'), bcrypt.gensalt())

    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Insertar el nuevo usuario con la contraseña encriptada
        cursor.execute(''' 
            INSERT INTO usuarios (username, contraseña, admin)
            VALUES (?, ?, 0)
        ''', (username, hashed_password))

        conn.commit()
        print(f"Usuario '{username}' registrado exitosamente.")
    except sqlite3.Error as e:
        print(f"Error al registrar el usuario: {e}")
    finally:
        conn.close()