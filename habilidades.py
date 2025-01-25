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
            duracion TEXT NOT NULL,
            casteo TEXT NOT NULL,
            descripcion TEXT NOT NULL,
            clase TEXT,
            raza TEXT,
            otro TEXT
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
            "descripcion": fila[4],
            "clase": fila[5],
            "raza": fila[6],
            "otro": fila[7]
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
def agregar_habilidad(nombre, coste, rango, descripcion, clase="", raza="", otro=""):
    if not re.match(r"^\d+(,\d+)*$", coste.strip()):
        print("El formato del coste no es válido. Debe ser del tipo S,M,R con S = Salud, M = Mana, R = Resistencia.")
        return

    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute(''' 
            INSERT INTO habilidades (nombre, coste, rango, descripcion, clase, raza, otro) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (nombre, coste, rango, descripcion, clase, raza, otro))

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