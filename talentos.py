import sqlite3
import os
import re
# Crear la tabla 'talentos'
def crear_tabla_talentos():
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS talentos (
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


def get_talento(nombre):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM talentos WHERE nombre = ?', (nombre,))
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

def get_all_talentos():
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM talentos')
        filas = cursor.fetchall()

        conn.close()

        talentos = [
            {
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
            for fila in filas
        ]
        return talentos

def agregar_talento(nombre, coste, rango, duracion, casteo, descripcion, efecto, clase=None, raza=None, otro=None):
        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()

            cursor.execute(''' 
                INSERT INTO talentos (nombre, coste, rango, duracion, casteo, descripcion,  clase, raza, otro) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (nombre, coste, rango, duracion, casteo, descripcion, clase, raza, otro))

            conn.commit()
            print("Talento agregado con éxito.")
        except sqlite3.IntegrityError:
            print(f"El talento '{nombre}' ya existe en la base de datos.")
        except sqlite3.Error as e:
            print(f"Error al agregar el talento a la base de datos: {e}")
        finally:
            conn.close()

def borrar_talento(id):
        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()

            cursor.execute('DELETE FROM talentos WHERE id = ?', (id,))
            conn.commit()
            print("Talento borrado con éxito.")
        except sqlite3.Error as e:
            print(f"Error al borrar el talento: {e}")
        finally:
            conn.close()

def modificar_talento(id, nombre=None, coste=None, rango=None, duracion=None, casteo=None, descripcion=None, clase=None, raza=None, otro=None):
        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()

            campos = []
            valores = []
            if nombre is not None:
                campos.append("nombre = ?")
                valores.append(nombre)
            if coste is not None:
                campos.append("coste = ?")
                valores.append(coste)
            if rango is not None:
                campos.append("rango = ?")
                valores.append(rango)
            if duracion is not None:
                campos.append("duracion = ?")
                valores.append(duracion)
            if casteo is not None:
                campos.append("casteo = ?")
                valores.append(casteo)
            if descripcion is not None:
                campos.append("descripcion = ?")
                valores.append(descripcion)
            if clase is not None:
                campos.append("clase = ?")
                valores.append(clase)
            if raza is not None:
                campos.append("raza = ?")
                valores.append(raza)
            if otro is not None:
                campos.append("otro = ?")
                valores.append(otro)

            if not campos:
                print("No se proporcionaron campos para actualizar.")
                return

            valores.append(id)
            sql = f"UPDATE talentos SET {', '.join(campos)} WHERE id = ?"
            cursor.execute(sql, valores)

            conn.commit()

            if cursor.rowcount > 0:
                print("Talento actualizado con éxito.")
            else:
                print(f"No se encontró un talento con el id '{id}', no se modificó nada.")
        except sqlite3.Error as e:
            print(f"Error al modificar el talento: {e}")
        finally:
            conn.close()
