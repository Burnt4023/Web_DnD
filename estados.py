import sqlite3
import os
import re

# Crear la tabla 'estados'
def crear_tabla_estados():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS estados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE,
            efecto TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


# Obtener un estado por nombre
def get_estado(nombre):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM estados WHERE nombre = ?', (nombre,))
    fila = cursor.fetchone()

    conn.close()

    if fila:
        return {
            "id": fila[0],
            "nombre": fila[1],
            "efecto": fila[2]
        }
    return None


# Obtener todos los estados
def get_all_estados():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT id, nombre, efecto FROM estados')
    filas = cursor.fetchall()

    conn.close()

    estados = [
        {
            "id": fila[0],
            "nombre": fila[1],
            "efecto": fila[2]
        }
        for fila in filas
    ]
    return estados


# Agregar un estado
def agregar_estado(nombre, efecto):
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute(''' 
            INSERT INTO estados (nombre, efecto) 
            VALUES (?, ?)
        ''', (nombre, efecto))

        conn.commit()
        print("Estado agregado con éxito.")
    except sqlite3.IntegrityError:
        print(f"El estado '{nombre}' ya existe en la base de datos.")
    except sqlite3.Error as e:
        print(f"Error al agregar el estado a la base de datos: {e}")
    finally:
        conn.close()


# Borrar un estado por ID
def borrar_estado(id):
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute('DELETE FROM estados WHERE id = ?', (id,))
        conn.commit()
        print("Estado borrado con éxito.")
    except sqlite3.Error as e:
        print(f"Error al borrar el estado: {e}")
    finally:
        conn.close()
