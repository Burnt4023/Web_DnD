import sqlite3
import os
import json


# Crear la tabla 'fichas'
def crear_tabla_fichas():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS fichas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            nombre TEXT NOT NULL,
            public BOOLEAN NOT NULL,
            foto TEXT
        )
    ''')

    # Crear índice único para evitar duplicados en 'username' y 'nombre'
    cursor.execute('''
        CREATE UNIQUE INDEX IF NOT EXISTS idx_fichas_username_nombre ON fichas(username, nombre)
    ''')

    conn.commit()
    conn.close()

    # Asegúrate de que la carpeta para las fichas exista
    if not os.path.exists('fichas'):
        os.makedirs('fichas')
        
    if not os.path.exists('fichas/fotos'):
        os.makedirs('fichas/fotos')
        
        
# Función para obtener las fichas por usuario
def obtener_fichas_por_usuario(username):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT id, nombre, public FROM fichas WHERE username = ?', (username,))
    fichas = cursor.fetchall()

    conn.close()
    return fichas

# Obtener fichas públicas de otros usuarios
def obtener_otras_fichas_publicas(username):
    try:
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, nombre, username FROM fichas WHERE username != ? AND public = true', (username,))
            fichas = cursor.fetchall()
            return fichas
    except sqlite3.Error as e:
        print(f"Error al acceder a la base de datos: {e}")
        return []

# Insertar una nueva ficha
def agregar_ficha(username, nombre, public, photo = ""):
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute(''' 
            INSERT INTO fichas (username, nombre, public, foto) 
            VALUES (?, ?, ?, ?)
        ''', (username, nombre, public, photo))

        conn.commit()
    except sqlite3.Error as e:
        print(f"Error al agregar la ficha: {e}")
    finally:
        conn.close()

# Obtener una ficha específica por nombre
def obtener_ficha_por_nombre(username, nombre_ficha):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT id, nombre, public FROM fichas WHERE username = ? AND nombre = ?', (username, nombre_ficha))
    ficha = cursor.fetchone()

    conn.close()
    return ficha

# Actualizar una ficha (cambiar su visibilidad)
def actualizar_ficha(username, nombre_ficha, public):
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute('''UPDATE fichas SET public = ? WHERE username = ? AND nombre = ?''', 
                       (public, username, nombre_ficha))
        conn.commit()

        # Verificar que la actualización se haya realizado
        if cursor.rowcount == 0:
            print(f"No se encontró la ficha {nombre_ficha} para el usuario {username}.")
    except sqlite3.Error as e:
        print(f"Error al actualizar la ficha: {e}")
    finally:
        conn.close()

def set_photo(username, nombre_ficha, photo):
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute('''UPDATE fichas SET foto = ? WHERE username = ? AND nombre = ?''', 
                       (photo, username, nombre_ficha))
        conn.commit()

        # Verificar que la actualización se haya realizado
        if cursor.rowcount == 0:
            print(f"No se encontró la ficha {nombre_ficha} para el usuario {username}.")
    except sqlite3.Error as e:
        print(f"Error al actualizar la ficha: {e}")
    finally:
        conn.close()

def get_photo(username, nombreficha):
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Consulta SQL para obtener la foto de la ficha
        cursor.execute('''SELECT foto FROM fichas WHERE username = ? AND nombre = ?''', 
                       (username, nombreficha))

        # Recuperar el resultado de la consulta
        result = cursor.fetchone()

        # Verificar si se encontró la ficha
        if result:
            return result[0]  # La foto está en el primer elemento de la tupla
        else:
            print(f"No se encontró la foto para la ficha {nombreficha} del usuario {username}.")
            return None
    except sqlite3.Error as e:
        print(f"Error al obtener la foto: {e}")
        return None
    finally:
        conn.close()
    
# Obtener el contenido de la ficha desde su archivo JSON
def obtener_contenido_de_archivo(username, nombre_ficha):
    """Obtiene el contenido de una ficha desde un archivo JSON y lo convierte en un diccionario."""
    ruta_archivo = f"fichas/{username}_{nombre_ficha}.json"
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            contenido = json.load(archivo)  # Leer y convertir a diccionario
        return contenido
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        return None


def guardar_contenido_en_archivo(username, nombre_ficha, contenido):
    """Guarda el contenido de una ficha en un archivo JSON."""
    ruta_archivo = f"fichas/{username}_{nombre_ficha}.json"
    try:
        with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
            json.dump(contenido, archivo, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        print(f"Error guardando ficha: {e}")
        return False
    

# Modificar el contenido de la ficha
def actualizar_ficha_en_bd(username, nombre_ficha, nuevo_contenido, public=False, photo=""):
    try:
        actualizar_ficha(username, nombre_ficha, public)
        set_photo(username, nombre_ficha, photo)
        exito = guardar_contenido_en_archivo(username, nombre_ficha, nuevo_contenido)
        return exito
    except Exception as e:
        print(f"Error actualizando ficha en BD: {e}")
        return False

# Mostrar el contenido de una ficha
def mostrar_contenido_ficha(username, nombre_ficha):
    contenido = obtener_contenido_de_archivo(username, nombre_ficha)
    if contenido:
        return contenido
    else:
        return "Contenido no disponible."
    
    
def eliminar_ficha(username, nombre_ficha):
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Verificar si la ficha existe antes de intentar eliminarla
        cursor.execute(''' 
            SELECT 1 FROM fichas WHERE username = ? AND nombre = ?
        ''', (username, nombre_ficha))
        if cursor.fetchone() is None:
            raise ValueError("La ficha no existe.")

        # Eliminar la ficha
        cursor.execute(''' 
            DELETE FROM fichas WHERE username = ? AND nombre = ?
        ''', (username, nombre_ficha))

        conn.commit()
        print(f"Ficha {nombre_ficha} eliminada exitosamente.")
    except sqlite3.Error as e:
        print(f"Error al eliminar la ficha en la base de datos: {e}")
    except ValueError as ve:
        print(ve)  # Ficha no encontrada
    finally:
        conn.close()
# Función para borrar el archivo que contiene el contenido de la ficha
def borrar_archivo_ficha(username, nombre_ficha):
    archivo_path = f'fichas/{username}_{nombre_ficha}.json'  # Ajusta la ruta según cómo se guardan los archivos
    if os.path.exists(archivo_path):
        os.remove(archivo_path)