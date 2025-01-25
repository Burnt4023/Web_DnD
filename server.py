from flask import Flask, render_template, request, redirect, url_for, session, flash
from usuarios import *
from fichas import *
from habilidades import *
from hechizos import *
from Objetos import *
import os

app = Flask(__name__)
app.secret_key = 'Keyzapzapzap'

# Aseguramos que las tablas necesarias existan al iniciar el servidor
crear_tabla_usuarios()
crear_tabla_fichas()
crear_tabla_habilidades()
crear_tabla_hechizos()
crear_tabla_armaduras()
crear_tabla_armas()
crear_tabla_objetos()


# Aseguramos que las fichas se almacenen en un directorio específico
def crear_directorio_fichas():
    if not os.path.exists('fichas'):
        os.makedirs('fichas')

# Lleva a login si no hay sesión, muestra home si hay
@app.route('/')
def home():
    if 'username' in session:
        return render_template('home.html')
    return redirect(url_for('login'))

# POST lleva a home, GET permite iniciar sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if validar_usuario(username, password):  # Validar usuario en la base de datos
            session['username'] = username
            return redirect(url_for('home'))
        else:
            flash('Usuario o contraseña incorrectos', 'error')
    return render_template('login.html')

# Cierra sesión
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

# GET muestra el formulario de registro, POST registra un nuevo usuario
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Comprobar si el nombre de usuario ya existe
        if obtener_usuario_por_nombre(username):
            flash('El nombre de usuario ya está en uso. Elige otro.', 'error')
        else:
            # Registrar el nuevo usuario
            registrar_usuario(username, password)
            flash('Usuario registrado exitosamente. Inicia sesión ahora.', 'success')
            return redirect(url_for('login'))

    return render_template('register.html')

# GET muestra las fichas del usuario actual, POST añade una nueva ficha
@app.route('/fichas', methods=['GET', 'POST'])
def fichas():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']

    if request.method == 'POST':
        nombre_ficha = request.form['nombre_ficha']
        contenido = request.form['contenido']

        # Agregar la ficha a la base de datos
        agregar_ficha(username, nombre_ficha, public=False)
        
        # Guardar el contenido de la ficha en un archivo
        guardar_contenido_en_archivo(username, nombre_ficha, contenido)

        flash('Ficha añadida exitosamente.', 'success')
        return redirect(url_for('fichas'))

    # Obtener las fichas del usuario actual
    fichas_usuario = obtener_fichas_por_usuario(username)

    # Obtener las fichas públicas de otras personas
    fichas_publicas = obtener_otras_fichas_publicas(username)

    return render_template('fichas.html', fichas_usuario=fichas_usuario, fichas_publicas=fichas_publicas)

@app.route('/fichas/ver/<nombre_ficha>/<owner_username>', methods=['GET'])
def ver_ficha(nombre_ficha, owner_username):
    if 'username' not in session:
        return redirect(url_for('login'))

    ficha = obtener_ficha_por_nombre(owner_username, nombre_ficha)
    if ficha is None or (not ficha[2] and owner_username != session["username"]):  # Comprobar acceso
        flash('La ficha no existe o no es pública.', 'error')
        return redirect(url_for('fichas'))

    try:
        contenido = obtener_contenido_de_archivo(owner_username, nombre_ficha)
    except FileNotFoundError:
        flash('El archivo de la ficha no se encontró.', 'error')
        return redirect(url_for('fichas'))

    # Obtener todas las habilidades de la base de datos
    habilidades_detalle = {}
    for habilidad in get_all_habilidades():
        habilidades_detalle[habilidad['nombre']] = {
            'coste': habilidad['coste'],
            'rango': habilidad['rango'],
            'descripcion': habilidad['descripcion'],
            'clase': habilidad['clase'],
            'raza': habilidad['raza'],
            'otro': habilidad['otro'],
            'duracion': str(habilidad.get('duracion', 'N/A')),
            'casteo': str(habilidad.get('casteo', 'N/A'))
        }

    # Obtener todos los hechizos de la base de datos
    hechizos_detalle = {}
    for hechizo in get_all_hechizos():
        hechizos_detalle[hechizo['nombre']] = {
            'nivel': hechizo['nivel'],
            'magia': hechizo['magia'],
            'coste': hechizo['coste'],
            'rango': hechizo['rango'],
            'duracion': str(hechizo.get('duracion', 'N/A')),
            'casteo': str(hechizo.get('casteo', 'N/A')),
            'clase': hechizo['clase'],
            'raza': hechizo['raza'],
            'otro': hechizo['otro'],
            'descripcion': hechizo['descripcion']
        }



    # Obtener todos los objetos de la base de datos (armas, armaduras, objetos)
    armas_detalle = []
    for arma in get_all_armas():
        armas_detalle.append({
            
            'nombre': arma['nombre'],
            'descripcion': arma['descripcion'],
            'daño': arma['daño'],  # Se usa 'daño' en lugar de 'coste'
            'calidad': arma['calidad'],  # Se usa 'calidad' en lugar de 'rango'
            'tipo': 'Arma'
        })

    # Detalles de armaduras
    armaduras_detalle = []
    for armadura in get_all_armaduras():
        armaduras_detalle.append({
            'nombre': armadura['nombre'],
            'descripcion': armadura['descripcion'],
            'rating': armadura['rating'],  # Se usa 'rating' en lugar de 'coste'
            'calidad': armadura['calidad'],  # Se usa 'calidad' en lugar de 'rango'
            'tipo': 'Armadura'
        })

    # Detalles de objetos
    objetos_detalle = []
    for objeto in get_all_objetos():
        objetos_detalle.append({
            'nombre': objeto['nombre'],
            'descripcion': objeto['descripcion'],
            'otros': objeto['otros'],  
        })


    
    return render_template(
        'ver_ficha.html',
        nombre_ficha=nombre_ficha,
        contenido=contenido,
        habilidades_detalle=habilidades_detalle,
        hechizos_detalle=hechizos_detalle,
        armas_detalle=armas_detalle,
        armaduras_detalle=armaduras_detalle,
        objetos_detalle=objetos_detalle
    )

@app.route('/fichas/modificar/<nombre_ficha>', methods=['GET', 'POST'])
def modificar_ficha(nombre_ficha):
    """Modifica una ficha existente."""
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']

    if request.method == 'POST':

        # Captura los datos del formulario
        campos_obligatorios = [
            'nombre_personaje', 'nivel', 'clase',
            'vida_actual', 'vida_maxima',
            'mana_actual', 'mana_maximo',
            'resistencia_actual', 'resistencia_maxima',
            'sobrecarga', 'velocidad', 'tiradas_exito', 'tiradas_fallo'
        ]

        # Validar que todos los campos obligatorios estén presentes
        datos_ficha = {campo: request.form.get(campo) for campo in campos_obligatorios}
        if not all(datos_ficha.values()):
            flash('Todos los campos son obligatorios.', 'error')
            return redirect(url_for('modificar_ficha', nombre_ficha=nombre_ficha))

        # Capturar el estado del checkbox de "ficha pública"
        ficha_publica = 'ficha_publica' in request.form  # True si el checkbox está marcado

        # Capturar habilidades, hechizos y objetos
        habilidades = request.form.getlist('habilidades[]')
        hechizos = request.form.getlist('hechizos[]')
        objetos = request.form.getlist('objetos[]')  # Nueva lista de objetos
        equipo = request.form.getlist('equipo[]')
        # Construir el nuevo contenido
        nuevo_contenido = {
            "nombre": datos_ficha['nombre_personaje'],
            "nivel": int(datos_ficha['nivel']),
            "clase": datos_ficha['clase'],
            "vida": {
                "actual": int(datos_ficha['vida_actual']),
                "maxima": int(datos_ficha['vida_maxima'])
            },
            "mana": {
                "actual": int(datos_ficha['mana_actual']),
                "maximo": int(datos_ficha['mana_maximo'])
            },
            "resistencia": {
                "actual": int(datos_ficha['resistencia_actual']),
                "maxima": int(datos_ficha['resistencia_maxima'])
            },
            "sobrecarga": int(datos_ficha['sobrecarga']),
            "velocidad": int(datos_ficha['velocidad']),
            "tiradas": {
                "exitos": int(datos_ficha['tiradas_exito']),
                "fallos": int(datos_ficha['tiradas_fallo'])
            },
            "habilidades": habilidades,  # Agregar habilidades
            "hechizos": hechizos,  # Agregar hechizos
            "objetos": objetos,  # Agregar objetos (armas, armaduras y objetos)
            "equipamiento": equipo,
            "publica": ficha_publica  # Agregar el valor de "publica" al contenido
        }

        # Actualizar la ficha en la base de datos
        actualizar_ficha_en_bd(username, nombre_ficha, nuevo_contenido, ficha_publica)

        flash('Ficha modificada exitosamente.', 'success')
        return redirect(url_for('fichas'))

    # Obtener los datos actuales de la ficha
    contenido = obtener_contenido_de_archivo(username, nombre_ficha)
    if contenido is None:
        flash('La ficha no existe o está dañada.', 'error')
        return redirect(url_for('fichas'))

    # Obtener todas las habilidades, hechizos, armas, armaduras y objetos posibles
    lista_habilidades = [habilidad['nombre'] for habilidad in get_all_habilidades()]
    lista_hechizos = [hechizo['nombre'] for hechizo in get_all_hechizos()]  # Lista de hechizos
    lista_armas = [arma['nombre'] for arma in get_all_armas()]  # Lista de armas
    lista_armaduras = [armadura['nombre'] for armadura in get_all_armaduras()]  # Lista de armaduras
    
    # Unificar armas, armaduras y otros objetos en una sola lista
    nombres_objetos = lista_armas + lista_armaduras + [objeto['nombre'] for objeto in get_all_objetos()]  # Lista de nombres de todos los objetos

    return render_template(
    'modificar_ficha.html',
    nombre_ficha=nombre_ficha,
    contenido=contenido,
    ficha_publica=contenido.get('publica', False),
    equipo=contenido.get('equipamiento', []),  # Pasar solo el equipo actual
    objetos=contenido.get('objetos', []),
    lista_habilidades=lista_habilidades,
    lista_hechizos=lista_hechizos,
    nombres_objetos=nombres_objetos
    )

@app.route('/fichas/crear', methods=['POST'])
def crear_ficha():
    if 'username' not in session:
        return {'success': False, 'error': 'No has iniciado sesión.'}, 401

    data = request.get_json()
    nombre_ficha = data.get('nombre_ficha')
    contenido = data.get('contenido')

    if not nombre_ficha:
        return {'success': False, 'error': 'El nombre de la ficha es obligatorio.'}, 400

    if not contenido:
        return {'success': False, 'error': 'El contenido de la ficha es obligatorio.'}, 400

    username = session['username']

    # Crear la ficha en la base de datos
    try:
        agregar_ficha(username, nombre_ficha, public=False)  # Usar tu función para agregar la ficha
        guardar_contenido_en_archivo(username, nombre_ficha, contenido)  # Guardar contenido en archivo
        return {'success': True}, 200
    except Exception as e:
        return {'success': False, 'error': str(e)}, 500
    
    
@app.route('/fichas/borrar/<nombre_ficha>', methods=['POST'])
def borrar_ficha(nombre_ficha):
    if 'username' not in session:
        flash('No has iniciado sesión.', 'error')  # Mensaje de error
        return redirect(url_for('login'))  # Redirigir al login

    username = session['username']

    try:
        # Primero, obtener la ficha de la base de datos
        ficha = obtener_ficha_por_nombre(username, nombre_ficha)
        if not ficha:
            flash('Ficha no encontrada.', 'error')  # Mensaje de error
            return redirect(url_for('fichas'))  # Redirigir a la página de fichas

        # Borrar la ficha de la base de datos
        eliminar_ficha(username, nombre_ficha)

        # Borrar el archivo que contiene los datos de la ficha
        borrar_archivo_ficha(username, nombre_ficha)

        flash('Ficha eliminada exitosamente.', 'success')  # Mensaje de éxito
        return redirect(url_for('fichas'))  # Redirigir a la página de fichas
    except Exception as e:
        flash(f'Error al eliminar la ficha: {str(e)}', 'error')  # Mensaje de error
        return redirect(url_for('fichas'))  # Redirigir a la página de fichas
    
if __name__ == '__main__':
    app.run(debug=True)