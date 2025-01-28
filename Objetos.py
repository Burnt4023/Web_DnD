import sqlite3
import os
import re

# Crear la tabla 'armas'
def crear_tabla_armas():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS armas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            daño TEXT NOT NULL,
            calidad INTEGER NOT NULL,
            otros TEXT,
            descripcion TEXT
        )
    ''')
    conn.commit()
    conn.close()


# Obtener un arma por nombre
def get_arma(nombre):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM armas WHERE nombre = ?', (nombre,))
    fila = cursor.fetchone()

    conn.close()

    if fila:
        return {
            "id": fila[0],
            "nombre": fila[1],
            "daño": fila[2],        # Daño en vez de coste
            "calidad": fila[3],     # Calidad en vez de rango
            "otros": fila[4],       # Otros detalles
            "descripcion": fila[5]  # Descripción
        }
    return None


# Obtener todas las armas
def get_all_armas():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT id, nombre, daño, calidad, otros, descripcion FROM armas')
    filas = cursor.fetchall()

    conn.close()

    armas = [
        {
            "id": fila[0],
            "nombre": fila[1],
            "daño": fila[2],
            "calidad": fila[3],
            "otros": fila[4],
            "descripcion": fila[5]
        }
        for fila in filas
    ]
    return armas


# Agregar un arma
def agregar_arma(nombre, daño, calidad, otros="", descripcion=""):
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute(''' 
            INSERT INTO armas (nombre, daño, calidad, otros, descripcion) 
            VALUES (?, ?, ?, ?, ?)
        ''', (nombre, daño, calidad, otros, descripcion))

        conn.commit()
        print("Arma agregada con éxito.")
    except sqlite3.Error as e:
        print(f"Error al agregar el arma a la base de datos: {e}")
    finally:
        conn.close()


# Borrar un arma por ID
def borrar_arma(id):
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute('DELETE FROM armas WHERE id = ?', (id,))
        conn.commit()
        print("Arma borrada con éxito.")
    except sqlite3.Error as e:
        print(f"Error al borrar el arma: {e}")
    finally:
        conn.close()
        
             
def crear_tabla_armaduras():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS armaduras (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            Rating TEXT NOT NULL,
            calidad INTEGER NOT NULL,
            otros TEXT,
            descripcion TEXT
        )
    ''')
    conn.commit()
    conn.close()





# Obtener una armadura por nombre
def get_armadura(nombre):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM armaduras WHERE nombre = ?', (nombre,))
    fila = cursor.fetchone()

    conn.close()
    if fila:
        return {
            "id": fila[0],
            "nombre": fila[1],
            "rating": fila[2],        # Rating en vez de daño
            "calidad": fila[3],       # Calidad
            "otros": fila[4],         # Otros detalles
            "descripcion": fila[5]    # Descripción
        }

    return None


# Obtener todas las armaduras
def get_all_armaduras():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT id, nombre, rating, calidad, otros, descripcion FROM armaduras')
    filas = cursor.fetchall()

    conn.close()

    armaduras = [
        {
            "id": fila[0],
            "nombre": fila[1],
            "rating": fila[2],
            "calidad": fila[3],
            "otros": fila[4],
            "descripcion": fila[5]
        }
        for fila in filas
    ]
    return armaduras


# Agregar una armadura
def agregar_armadura(nombre, rating, calidad, otros="", descripcion=""):
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute(''' 
            INSERT INTO armaduras (nombre, rating, calidad, otros, descripcion) 
            VALUES (?, ?, ?, ?, ?)
        ''', (nombre, rating, calidad, otros, descripcion))

        conn.commit()
        print("Armadura agregada con éxito.")
    except sqlite3.Error as e:
        print(f"Error al agregar la armadura a la base de datos: {e}")
    finally:
        conn.close()


# Borrar una armadura por ID
def borrar_armadura(id):
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute('DELETE FROM armaduras WHERE id = ?', (id,))
        conn.commit()
        print("Armadura borrada con éxito.")
    except sqlite3.Error as e:
        print(f"Error al borrar la armadura: {e}")
    finally:
        conn.close()






# Crear la tabla 'objetos'
def crear_tabla_objetos():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS objetos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            otros TEXT,
            descripcion TEXT
        )
    ''')
    conn.commit()
    conn.close()


# Obtener un objeto por nombre
def get_objeto(nombre):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM objetos WHERE nombre = ?', (nombre,))
    fila = cursor.fetchone()

    conn.close()

    if fila:
        return {
            "id": fila[0],
            "nombre": fila[1],
            "otros": fila[2],        # Otros detalles
            "descripcion": fila[3]   # Descripción
        }
    return None


# Obtener todos los objetos
def get_all_objetos():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT id, nombre, otros, descripcion FROM objetos')
    filas = cursor.fetchall()

    conn.close()

    objetos = [
        {
            "id": fila[0],
            "nombre": fila[1],
            "otros": fila[2],
            "descripcion": fila[3]
        }
        for fila in filas
    ]
    return objetos


# Agregar un objeto
def agregar_objeto(nombre, otros="", descripcion=""):
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute(''' 
            INSERT INTO objetos (nombre, otros, descripcion) 
            VALUES (?, ?, ?)
        ''', (nombre, otros, descripcion))

        conn.commit()
        print("Objeto agregado con éxito.")
    except sqlite3.Error as e:
        print(f"Error al agregar el objeto a la base de datos: {e}")
    finally:
        conn.close()


# Borrar un objeto por ID
def borrar_objeto(id):
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute('DELETE FROM objetos WHERE id = ?', (id,))
        conn.commit()
        print("Objeto borrado con éxito.")
    except sqlite3.Error as e:
        print(f"Error al borrar el objeto: {e}")
    finally:
        conn.close()