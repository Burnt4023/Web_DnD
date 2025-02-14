from flask import Flask, render_template, render_template_string, request, redirect, url_for, session, flash, send_from_directory
from usuarios import *
from fichas import *
from habilidades import *
from hechizos import *
from Objetos import *
from estados import *
import os

app = Flask(__name__)
app.secret_key = 'Keyzapzapzap'
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'fichas', 'fotos')

# Aseguramos que las tablas necesarias existan al iniciar el servidor
crear_tabla_usuarios()
crear_tabla_fichas()
crear_tabla_habilidades()
crear_tabla_hechizos()
crear_tabla_armaduras()
crear_tabla_armas()
crear_tabla_objetos()
crear_tabla_estados()



# Lleva a login si no hay sesión, muestra home si hay
@app.route('/')
def home():
    if 'username' in session:
        return render_template('home.html')
    return redirect(url_for('login'))

@app.route('/fichas/fotos/<path:filename>')
def serve_photo(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)



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
        if habilidad['nombre'] in contenido['habilidades']:
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
        if hechizo['nombre'] in contenido['hechizos']:
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
        if arma['nombre'] in contenido['objetos']:
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
        if armadura['nombre'] in contenido['objetos']:
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
        if objeto['nombre'] in contenido['objetos']:
            objetos_detalle.append({
                'nombre': objeto['nombre'],
                'descripcion': objeto['descripcion'],
                'otros': objeto['otros'],  
            })

    estados_detalle = []
    for estado in get_all_estados():
        if estado['nombre'] in contenido['estados']:
            estados_detalle.append({
                'nombre': estado['nombre'],
                'efecto': estado['efecto'],
            })
    return render_template(
        'ver_ficha.html',
        nombre_ficha=nombre_ficha,
        contenido=contenido,
        habilidades_detalle=habilidades_detalle,
        hechizos_detalle=hechizos_detalle,
        armas_detalle=armas_detalle,
        armaduras_detalle=armaduras_detalle,
        objetos_detalle=objetos_detalle,
        estados_detalle=estados_detalle
    )

@app.route('/fichas/modificar/<nombre_ficha>', methods=['GET', 'POST'])
def modificar_ficha(nombre_ficha):
    """Modifica una ficha existente."""
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']

    if request.method == 'POST':
        # Definir todos los campos de la ficha
        campos = [
            'nombre_personaje', 'nivel', 'clase', 'magia', 'talento', 'alineamiento', 'historia', 'foto',
            'vida_actual', 'vida_maxima', 'mana_actual', 'mana_maximo', 'resistencia_actual', 'resistencia_maxima',
            'sobrecarga', 'velocidad', 'armadura', 'iniciativa', 'tiradas_exito', 'tiradas_fallo'
        ]

        # Capturar los datos del formulario con valores por defecto
        datos_ficha = {campo: request.form.get(campo, None) for campo in campos}
        
        
        
        
        
        
        
        # Capturar el estado del checkbox de "ficha pública"
        ficha_publica = 'ficha_publica' in request.form  # True si el checkbox está marcado

        # Capturar habilidades, hechizos y objetos
        habilidades = request.form.getlist('habilidades[]')
        hechizos = request.form.getlist('hechizos[]')
        objetos = request.form.getlist('objetos[]')
        equipo = request.form.getlist('equipo[]')
        estados = request.form.getlist('estados[]')
        

        fotoname = ""
        # Verificar si se subió una nueva foto
        foto = request.files.get('foto')

        # Si se sube una nueva foto
        if foto:
            # Crear el nombre de archivo con un formato único (usando el username y nombre del personaje)
            fotoname = f"{username}_{datos_ficha['nombre_personaje']}.{foto.filename.split('.')[-1].lower()}"
            foto.save(os.path.join(UPLOAD_FOLDER, fotoname))  # Guardar la foto en la carpeta de subida
        else:
            # Si no se sube una nueva foto, mantener la foto anterior
            fotoname = get_photo(username, nombre_ficha)

        # Captura de destrezas
        destrezas = [int(request.form.get(f"destrezas[{i}]", 15)) for i in range(16)]

        # Captura de estadísticas
        estadisticas = [int(request.form.get(f"estadisticas[{i}]", 0)) for i in range(9)]

        # Captura de los valores de dinero enviados por el formulario
        dinero = request.form.getlist('dinero[]')
        cobre = int(dinero[0]) if len(dinero) > 0 else 0
        plata = int(dinero[1]) if len(dinero) > 1 else 0
        oro = int(dinero[2]) if len(dinero) > 2 else 0
        platino = int(dinero[3]) if len(dinero) > 3 else 0

        # Construcción del nuevo contenido de la ficha
        nuevo_contenido = {
            "nombre": datos_ficha['nombre_personaje'],
            "nivel": int(datos_ficha['nivel']) if datos_ficha['nivel'] else 1,
            "clase": datos_ficha['clase'] or 'Sin clase',
            "magia": datos_ficha['magia'] or 'Ninguna',
            "talento": datos_ficha['talento'] or 'Ninguno',
            "alineamiento": datos_ficha['alineamiento'] or 'Neutral',
            "historia": datos_ficha['historia'] or 'No',
            "foto": fotoname,  # Usar la URL de la foto
            "iniciativa": datos_ficha['iniciativa'],
            "vida": {
                "actual": int(datos_ficha['vida_actual']) if datos_ficha['vida_actual'] else 10,
                "maxima": int(datos_ficha['vida_maxima']) if datos_ficha['vida_maxima'] else 10
            },
            "mana": {
                "actual": int(datos_ficha['mana_actual']) if datos_ficha['mana_actual'] else 10,
                "maximo": int(datos_ficha['mana_maximo']) if datos_ficha['mana_maximo'] else 10
            },
            "resistencia": {
                "actual": int(datos_ficha['resistencia_actual']) if datos_ficha['resistencia_actual'] else 10,
                "maxima": int(datos_ficha['resistencia_maxima']) if datos_ficha['resistencia_maxima'] else 10
            },
            "sobrecarga": int(datos_ficha['sobrecarga']) if datos_ficha['sobrecarga'] else 0,
            "velocidad": int(datos_ficha['velocidad']) if datos_ficha['velocidad'] else 30,
            "armadura": int(datos_ficha['armadura']) if datos_ficha['armadura'] else 10,
            "iniciativa": int(datos_ficha['iniciativa']) if datos_ficha['iniciativa'] else 0,
            "tiradas": {
                "exitos": int(datos_ficha['tiradas_exito']) if datos_ficha['tiradas_exito'] else 0,
                "fallos": int(datos_ficha['tiradas_fallo']) if datos_ficha['tiradas_fallo'] else 0
            },
            "habilidades": habilidades,
            "hechizos": hechizos,
            "objetos": objetos,
            "equipamiento": equipo,
            "destrezas": destrezas,
            "estadisticas": estadisticas,
            "estados": estados,
            "dinero": [cobre, plata, oro, platino],
            "publica": ficha_publica
        }

        # Actualizar la ficha en la base de datos
        actualizar_ficha_en_bd(username, nombre_ficha, nuevo_contenido, ficha_publica, fotoname)

        flash('Ficha modificada exitosamente.', 'success')
        return redirect(url_for('ver_ficha', nombre_ficha=nombre_ficha, owner_username=session['username']))

    # Obtener los datos actuales de la ficha
    contenido = obtener_contenido_de_archivo(username, nombre_ficha)
    if contenido is None:
        flash('La ficha no existe o está dañada.', 'error')
        return redirect(url_for('fichas'))

    # Obtener todas las habilidades, hechizos, armas, armaduras y objetos posibles
    lista_habilidades = [habilidad['nombre'] for habilidad in get_all_habilidades()]
    lista_hechizos = [hechizo['nombre'] for hechizo in get_all_hechizos()]
    lista_armas = [arma['nombre'] for arma in get_all_armas()]
    lista_armaduras = [armadura['nombre'] for armadura in get_all_armaduras()]
    lista_estados = [estado['nombre'] for estado in get_all_estados()]
    nombres_objetos = lista_armas + lista_armaduras + [objeto['nombre'] for objeto in get_all_objetos()]

    return render_template(
        'modificar_ficha.html',
        nombre_ficha=nombre_ficha,
        contenido=contenido,
        ficha_publica=contenido.get('publica', False),
        equipo=contenido.get('equipamiento', []),
        objetos=contenido.get('objetos', []),
        lista_habilidades=lista_habilidades,
        lista_hechizos=lista_hechizos,
        lista_estados=lista_estados,
        nombres_objetos=nombres_objetos,
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


@app.route('/wiki')
def wiki():
    if 'username' in session:
        return render_template('wiki/wiki_home.html')
    return redirect(url_for('login'))   


@app.route('/wiki/objetos')
def wiki_objetos():
    if 'username' in session:
        # Obtener los objetos de la base de datos
        armas = get_all_armas()  # Esta función devuelve una lista de objetos
        armaduras = get_all_armaduras()
        objetos = get_all_objetos()
        
        return render_template('wiki/objetos.html', armas=armas, armaduras=armaduras, objetos=objetos)
    
    return redirect(url_for('login')) 

@app.route('/wiki/arma/<arma_nombre>')
def wiki_arma(arma_nombre):
    # Obtener el arma por su nombre
    arma = get_arma(arma_nombre)

    if not arma:
        return f"Arma '{arma_nombre}' no encontrada."

    # Generamos el HTML dinámicamente con los parámetros del arma
    html_content = f"""
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{arma['nombre']}</title>
    </head>
    <body>
        <h1>{arma['nombre']}</h1>
        <p><strong>Descripción:</strong> {arma['descripcion']}</p>
        <p><strong>Daño:</strong> {arma['daño']}</p>
        <p><strong>Calidad:</strong> {arma['calidad']}</p>
        <p><strong>Otros detalles:</strong> {arma['otros']}</p>
        <a href="/wiki">Volver a la lista de armas</a>
    </body>
    </html>
    """
    
    return render_template_string(html_content)


@app.route('/wiki/armadura/<armadura_nombre>')
def wiki_armadura(armadura_nombre):
    # Obtener la armadura por su nombre
    armadura = get_armadura(armadura_nombre)

    if not armadura:
        return f"Armadura '{armadura_nombre}' no encontrada."
    
    # Generamos el HTML dinámicamente con los parámetros de la armadura
    html_content = f"""
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{armadura['nombre']}</title>
    </head>
    <body>
        <h1>{armadura['nombre']}</h1>
        <p><strong>Descripción:</strong> {armadura['descripcion']}</p>
        <p><strong>Rating:</strong> {armadura['rating']}</p>
        <p><strong>Calidad:</strong> {armadura['calidad']}</p>
        <p><strong>Otros detalles:</strong> {armadura['otros']}</p>
        <a href="/wiki">Volver a la lista de armaduras</a>
    </body>
    </html>
    """
    
    return render_template_string(html_content)


@app.route('/wiki/objeto/<objeto_nombre>')
def wiki_objeto(objeto_nombre):
    # Obtener el objeto por su nombre
    objeto = get_objeto(objeto_nombre)

    if not objeto:
        return f"Objeto '{objeto_nombre}' no encontrado."

    # Generamos el HTML dinámicamente con los parámetros del objeto
    html_content = f"""
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{objeto['nombre']}</title>
    </head>
    <body>
        <h1>{objeto['nombre']}</h1>
        <p><strong>Descripción:</strong> {objeto['descripcion']}</p>
        <p><strong>Otros detalles:</strong> {objeto['otros']}</p>
        <a href="/wiki">Volver a la lista de objetos</a>
    </body>
    </html>
    """
    
    return render_template_string(html_content)

@app.route('/wiki/hechizos')
def wiki_hechizos():
    if 'username' not in session:
        flash('No has iniciado sesión.', 'error')  # Mensaje de error
        return redirect(url_for('login'))  # Redirigir al login
    hechizos = get_all_hechizos_por_clase()
    return render_template('wiki/hechizos.html', hechizos = hechizos)


@app.route('/wiki/hechizo/<hechizo_nombre>')
def wiki_hechizo(hechizo_nombre):
    # Lógica para obtener el hechizo por su nombre y mostrarlo
    hechizo = get_hechizo(hechizo_nombre)
    if not hechizo:
        return f"Hechizo '{hechizo_nombre}' no encontrado."

    # Desglosar el coste en vida, mana y resistencia (suponiendo que coste es una cadena 'x,y,z')
    coste_vida, coste_mana, coste_resistencia = hechizo['coste'].split(',')

    # Generamos el HTML dinámicamente con los parámetros del hechizo
    html_content = f"""
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{hechizo['nombre']}</title>
    </head>
    <body>
        <h1>{hechizo['nombre']}</h1>
        <p><strong>Descripción:</strong> {hechizo['descripcion']}</p>
        <p><strong>Nivel:</strong> {hechizo['nivel']}</p>
        <p><strong>Magia:</strong> {hechizo['magia']}</p>
        <p><strong>Coste de vida:</strong> {coste_vida}</p>
        <p><strong>Coste de mana:</strong> {coste_mana}</p>
        <p><strong>Coste de resistencia:</strong> {coste_resistencia}</p>
        <p><strong>Rango:</strong> {hechizo['rango']}</p>
        <p><strong>Duración:</strong> {hechizo['duracion']}</p>
        <p><strong>Casteo:</strong> {hechizo['casteo']}</p>
        <p><strong>Clase:</strong> {hechizo['clase']}</p>
        <p><strong>Raza:</strong> {hechizo['raza']}</p>
        <p><strong>Otros:</strong> {hechizo['otro']}</p>
        <a href="/wiki/hechizos">Volver a la lista de hechizos</a>
    </body>
    </html>
    """
    
    return render_template_string(html_content)



@app.route('/wiki/habilidades')
def wiki_habilidades():
    # Obtener todas las habilidades
    habilidades = get_all_habilidades()  # Función que obtiene todas las habilidades de la base de datos
    
    if not habilidades:
        return "No se encontraron habilidades."

    # Renderizar la plantilla con las habilidades
    return render_template('wiki/habilidades.html', habilidades=habilidades)

@app.route('/wiki/habilidad/<habilidad_nombre>')
def wiki_habilidad(habilidad_nombre):
    # Lógica para obtener la habilidad por su nombre y mostrarla
    habilidad = get_habilidad(habilidad_nombre)
    if not habilidad:
        return f"Habilidad '{habilidad_nombre}' no encontrada."

    # Desglosar el coste en vida, mana y resistencia (suponiendo que coste es una cadena 'x,y,z')
    coste_vida, coste_mana, coste_resistencia = habilidad['coste'].split(',')

    # Generamos el HTML dinámicamente con los parámetros de la habilidad
    html_content = f"""
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{habilidad['nombre']}</title>
    </head>
    <body>
        <h1>{habilidad['nombre']}</h1>
        <p><strong>Descripción:</strong> {habilidad['descripcion']}</p>
        <p><strong>Coste de vida:</strong> {coste_vida}</p>
        <p><strong>Coste de mana:</strong> {coste_mana}</p>
        <p><strong>Coste de resistencia:</strong> {coste_resistencia}</p>
        <p><strong>Rango:</strong> {habilidad['rango']}</p>
        <p><strong>Duración:</strong> {habilidad['duracion']}</p>
        <p><strong>Casteo:</strong> {habilidad['casteo']}</p>
        <p><strong>Clase:</strong> {habilidad['clase']}</p>
        <p><strong>Otros detalles:</strong> {habilidad['otro']}</p>
        <a href="/wiki/habilidades">Volver a la lista de habilidades</a>
    </body>
    </html>
    """
    
    return render_template_string(html_content)

@app.route('/wiki/crear_personaje')
def wiki_crear_personaje():
    if 'username' not in session:
        flash('No has iniciado sesión.', 'error')  # Mensaje de error
        return redirect(url_for('login'))  # Redirigir al login
    
    
    return render_template('wiki/personaje.html')


@app.route('/wiki/clases')
def wiki_clases():
    if 'username' not in session:
        flash('No has iniciado sesión.', 'error')  # Mensaje de error
        return redirect(url_for('login'))  # Redirigir al login
    
    
    return render_template('wiki/clases/clases.html')



# ENTRADAS PARA HECHICEROS
########################################################################################
@app.route('/wiki/mago/hechicero')
def wiki_hechicero():
    if 'username' not in session:
        flash('No has iniciado sesión.', 'error')  # Mensaje de error
        return redirect(url_for('login'))  # Redirigir al login
    return render_template('wiki/clases/mago/hechicero/hechicero.html')

@app.route('/wiki/mago/hechicero/herencia_draconica')
def wiki_hechicero_draconido():
    if 'username' not in session:
        flash('No has iniciado sesión.', 'error')  # Mensaje de error
        return redirect(url_for('login'))  # Redirigir al login
    
    
    return render_template('wiki/clases/mago/hechicero/herencia_draconica.html')

@app.route('/wiki/mago/hechicero/superviviente_cataclismo')
def wiki_hechicero_cataclismo():
    if 'username' not in session:
        flash('No has iniciado sesión.', 'error')  # Mensaje de error
        return redirect(url_for('login'))  # Redirigir al login
    
    
    return render_template('wiki/clases/mago/hechicero/superviviente_cataclismo.html')

@app.route('/wiki/mago/hechicero/engendro_caos')
def wiki_hechicero_engendro():
    if 'username' not in session:
        flash('No has iniciado sesión.', 'error')  # Mensaje de error
        return redirect(url_for('login'))  # Redirigir al login
    
    
    return render_template('wiki/clases/mago/hechicero/engendro_caos.html')

@app.route('/wiki/mago/hechicero/herencia_necroplaga')
def wiki_hechicero_necroplaga():
    if 'username' not in session:
        flash('No has iniciado sesión.', 'error')  # Mensaje de error
        return redirect(url_for('login'))  # Redirigir al login
    
    
    return render_template('wiki/clases/mago/hechicero/herencia_necroplaga.html')

@app.route('/wiki/mago/hechicero/azote_estrellas')
def wiki_hechicero_estrellas():
    if 'username' not in session:
        flash('No has iniciado sesión.', 'error')  # Mensaje de error
        return redirect(url_for('login'))  # Redirigir al login
    
    
    return render_template('wiki/clases/mago/hechicero/azote_estrellas.html')

@app.route('/wiki/mago/hechicero/sin_origen')
def wiki_hechicero_custom():
    if 'username' not in session:
        flash('No has iniciado sesión.', 'error')  # Mensaje de error
        return redirect(url_for('login'))  # Redirigir al login
    
    
    return render_template('wiki/clases/mago/hechicero/custom/custom.html')
########################################################################################

# ENTRADAS PARA CLERIGOS
@app.route('/wiki/mago/clerigo')
def wiki_clerigo():
    if 'username' not in session:
        flash('No has iniciado sesión.', 'error')  # Mensaje de error
        return redirect(url_for('login'))  # Redirigir al login
    return render_template('wiki/clases/mago/clerigo/clerigo.html')




# ENTRADAS PARA GUERRERO
@app.route('/wiki/guerrero/ronin')
def wiki_ronin():
    if 'username' not in session:
        flash('No has iniciado sesión.', 'error')  # Mensaje de error
        return redirect(url_for('login'))  # Redirigir al login
    return render_template('wiki/clases/guerrero/ronin/ronin.html')

@app.route('/wiki/guerrero/paladin')
def wiki_paladin():
    if 'username' not in session:
        flash('No has iniciado sesión.', 'error')  # Mensaje de error
        return redirect(url_for('login'))  # Redirigir al login
    return render_template('wiki/clases/guerrero/paladin/paladin.html')

@app.route('/wiki/guerrero/barbaro')
def wiki_barbaro():
    if 'username' not in session:
        flash('No has iniciado sesión.', 'error')  # Mensaje de error
        return redirect(url_for('login'))  # Redirigir al login
    return render_template('wiki/clases/guerrero/barbaro/barbaro.html')




#ENTRADAS PARA PICARO
@app.route('/wiki/picaro/asesino')
def wiki_asesino():
    if 'username' not in session:
        flash('No has iniciado sesión.', 'error')  # Mensaje de error
        return redirect(url_for('login'))  # Redirigir al login
    return render_template('wiki/clases/picaro/asesino/asesino.html')

@app.route('/wiki/picaro/monje')
def wiki_monje():
    if 'username' not in session:
        flash('No has iniciado sesión.', 'error')  # Mensaje de error
        return redirect(url_for('login'))  # Redirigir al login
    return render_template('wiki/clases/picaro/monje/monje.html')

@app.route('/wiki/picaro/bardo')
def wiki_bardo():
    if 'username' not in session:
        flash('No has iniciado sesión.', 'error')  # Mensaje de error
        return redirect(url_for('login'))  # Redirigir al login
    return render_template('wiki/clases/picaro/bardo/bardo.html')

@app.route('/wiki/picaro/explorador')
def wiki_explorador():
    if 'username' not in session:
        flash('No has iniciado sesión.', 'error')  # Mensaje de error
        return redirect(url_for('login'))  # Redirigir al login
    return render_template('wiki/clases/picaro/explorador/explorador.html')





@app.route('/wiki/razas')
def wiki_razas():
    if 'username' not in session:
        flash('No has iniciado sesión.', 'error')  # Mensaje de error
        return redirect(url_for('login'))  # Redirigir al login
    

    return render_template('wiki/razas.html')

if __name__ == '__main__':
    app.run(debug=True)