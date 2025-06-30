import sqlite3
import os
import re

# Crear la tabla 'habilidades'
def crear_tabla_habilidades():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS habilidades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            coste TEXT NOT NULL,
            rango INTEGER NOT NULL,
            tipo TEXT NOT NULL,
            descripcion TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()



# Obtener una habilidad por nombre
def get_habilidad(nombre):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM habilidades WHERE nombre = ?', (nombre,))
    fila = cursor.fetchone()

    conn.close()

    if fila:
        return {
            "id": fila[0],
            "nombre": fila[1],
            "coste": fila[2],
            "rango": fila[3],
            "duracion": fila[4],
            "casteo": fila[5],
            "descripcion": fila[6],
            "clase": fila[7],
            "raza": fila[8],
            "otro": fila[9]
        }
    return None


# Obtener todas las habilidades
def get_all_habilidades():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT id, nombre, coste, rango, descripcion, clase, raza, otro, duracion, casteo FROM habilidades')
    filas = cursor.fetchall()

    conn.close()

    habilidades = [
        {
            "id": fila[0],
            "nombre": fila[1],
            "coste": fila[2],
            "rango": fila[3],
            "descripcion": fila[4],  # Ahora fila[4] es descripcion
            "clase": fila[5],        # Ahora fila[5] es clase
            "raza": fila[6],         # Ahora fila[6] es raza
            "otro": fila[7],         # Ahora fila[7] es otro
            "duracion": fila[8],     # Ahora fila[8] es duracion
            "casteo": fila[9]        # Ahora fila[9] es casteo
        }
        for fila in filas
    ]
    return habilidades


# Agregar una habilidad
def agregar_habilidad(nombre, coste, rango, duracion, casteo, descripcion, clase="", raza="", otro=""):
    # Validación del coste
    if not re.match(r"^\d+(,\d+)*$", coste.strip()):
        print("El formato del coste no es válido. Debe ser del tipo S,M,R con S = Salud, M = Mana, R = Resistencia.")
        return

    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Insertar los datos en la base de datos
        cursor.execute(''' 
            INSERT INTO habilidades (nombre, coste, rango, duracion, casteo, descripcion, clase, raza, otro) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (nombre, coste, rango, duracion, casteo, descripcion, clase, raza, otro))

        conn.commit()
        print("Habilidad agregada con éxito.")
    except sqlite3.Error as e:
        print(f"Error al agregar la habilidad a la base de datos: {e}")
    finally:
        conn.close()


# Borrar una habilidad por ID
def borrar_habilidad(id):
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute('DELETE FROM habilidades WHERE id = ?', (id,))
        conn.commit()
        print("Habilidad borrada con éxito.")
    except sqlite3.Error as e:
        print(f"Error al borrar la habilidad: {e}")
    finally:
        conn.close()
        
def modificar_habilidad(nombre_original, nombre, coste, rango, duracion, casteo, descripcion, clase, raza, otro):
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Ejecutar la actualización en la base de datos
        cursor.execute('''
            UPDATE habilidades
            SET nombre = ?, coste = ?, rango = ?, duracion = ?, casteo = ?, descripcion = ?, clase = ?, raza = ?, otro = ?
            WHERE nombre = ?
        ''', (nombre, coste, rango, duracion, casteo, descripcion, clase, raza, otro, nombre_original))

        conn.commit()

        # Verificar si realmente se actualizó alguna fila
        if cursor.rowcount > 0:
            print(f"Habilidad '{nombre_original}' actualizada con éxito.")
        else:
            print(f"No se encontró una habilidad con el nombre '{nombre_original}', no se modificó nada.")

    except sqlite3.Error as e:
        print(f"Error al modificar la habilidad: {e}")
    finally:
        conn.close()