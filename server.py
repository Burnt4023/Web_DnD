from flask import Flask, render_template, render_template_string, request, redirect, url_for, session, flash, send_from_directory
from usuarios import *
from fichas import *
from habilidades import *
#from hechizos import *
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
#crear_tabla_hechizos()
crear_tabla_armaduras()
crear_tabla_armas()
crear_tabla_objetos()
crear_tabla_estados()



# Lleva a login si no hay sesión, muestra home si hay
@app.route('/')
def home():
    if 'username' in session:
        usuario = obtener_usuario_por_nombre(session['username'])
        return render_template('home.html', usuario=usuario)
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

@app.route('/fichas/ver/<owner_username>/<nombre_ficha>', methods=['GET'])
def ver_ficha(owner_username, nombre_ficha):
    if 'username' not in session:
        return redirect(url_for('login'))

    contenido = obtener_contenido_de_archivo(owner_username, nombre_ficha)

    if contenido is None:
        return "Ficha no encontrada o archivo corrupto", 404

    return render_template(
        'ver_ficha.html',
        nombre_ficha=nombre_ficha,
        contenido=contenido
    )

@app.route('/fichas/modificar/<nombre_ficha>', methods=['GET', 'POST'])
def modificar_ficha(nombre_ficha):
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']

    if request.method == 'GET':
        contenido = obtener_contenido_de_archivo(username, nombre_ficha)
        return render_template(
            'modificar_ficha.html',
            nombre_ficha=nombre_ficha,
            contenido=contenido,
        )

    if request.method == 'POST':
        # Campos simples
        nombre = request.form.get('nombre', nombre_ficha)
        nivel = int(request.form.get('nivel', 1))
        clase = request.form.get('clase', 'Sin clase')
        magia = request.form.get('magia', 'Ninguna')
        talento = request.form.get('talento', 'Ninguno')
        alineamiento = request.form.get('alineamiento', 'Neutral')
        historia = request.form.get('historia', 'No')
        


        fotoname = ""
        # Verificar si se subió una nueva foto
        foto = request.files.get('foto')

        # Si se sube una nueva foto
        if foto:
            # Crear el nombre de archivo con un formato único (usando el username y nombre del personaje)
            fotoname = f"{username}_{request.form.get('nombreFicha')}.{foto.filename.split('.')[-1].lower()}"
            foto.save(os.path.join(UPLOAD_FOLDER, fotoname))  # Guardar la foto en la carpeta de subida
        else:
            # Si no se sube una nueva foto, mantener la foto anterior
            fotoname = get_photo(username, nombre_ficha)

        

        # Campos compuestos
        vida_actual = int(request.form.get('vida_actual', 10))
        vida_maximo = int(request.form.get('vida_maxima', 10))
        mana_actual = int(request.form.get('mana_actual', 10))
        mana_maximo = int(request.form.get('mana_maxima', 10))
        stamina_actual = int(request.form.get('resistencia_actual', 10))
        stamina_maximo = int(request.form.get('resistencia_maxima', 10))

        sobrecarga = int(request.form.get('sobrecarga', 0))
        velocidad = int(request.form.get('velocidad', 30))
        armadura = int(request.form.get('armadura', 10))
        iniciativa = int(request.form.get('iniciativa', 0))

        # Listas: espera que lleguen como cadenas separadas por comas
        proficiencias_str = request.form.get('proficiencias', '15,15,15,15,15,15,15,15,15')
        proficiencias = [int(x) for x in proficiencias_str.split(',') if x.strip().isdigit()]

        estadisticas = [int(request.form.get(f'estadisticas[{i}]', '0')) for i in range(9)]

        ficha_publica = 'ficha_publica' in request.form
        # Listas complejas que probablemente deban venir en JSON string
        import json
        habilidades = []
        estados = []
        objetos = []
        equipamiento = []
        dinero = [0, 0, 0, 0]

        try:
            habilidades = json.loads(request.form.get('habilidades', '[]'))
            estados = json.loads(request.form.get('estados', '[]'))
            objetos = json.loads(request.form.get('objetos', '[]'))
            equipamiento = json.loads(request.form.get('equipamiento', '[]'))
            dinero = json.loads(request.form.get('dinero', '[0,0,0,0]'))
        except Exception:
            pass  # Si no viene bien, quedan vacíos o default

        datos_ficha = {
            "nombre": nombre,
            "nivel": nivel,
            "clase": clase,
            "magia": magia,
            "talento": talento,
            "alineamiento": alineamiento,
            "vida": {"actual": vida_actual, "maximo": vida_maximo},
            "mana": {"actual": mana_actual, "maximo": mana_maximo},
            "stamina": {"actual": stamina_actual, "maximo": stamina_maximo},
            "sobrecarga": sobrecarga,
            "velocidad": velocidad,
            "armadura": armadura,
            "iniciativa": iniciativa,
            "historia": historia,
            "foto": fotoname,
            "Proficiencias": proficiencias,
            "estadisticas": estadisticas,
            "habilidades": habilidades,
            "estados": estados,
            "objetos": objetos,
            "equipamiento": equipamiento,
            "dinero": dinero
        }

        # Guardar el JSON con función que implementes
        exito = actualizar_ficha_en_bd(username, nombre_ficha, datos_ficha, ficha_publica, fotoname)
        if not exito:
            return "Error al guardar la ficha", 500

        return redirect(url_for('ver_ficha', owner_username=username, nombre_ficha=nombre_ficha))
    

    
    
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




# APARTADO PARA OBJETOS
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
#####################################################################






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

@app.route('/wiki/mago/clerigo/yses')
def wiki_clerigo_yses():
    if 'username' not in session:
        flash('No has iniciado sesión.', 'error')  # Mensaje de error
        return redirect(url_for('login'))  # Redirigir al login
    return render_template('wiki/clases/mago/clerigo/Yses.html')

###############################################




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

@app.route('/wiki/magia')
def wiki_magia():
    if 'username' not in session:
        flash('No has iniciado sesión.', 'error')  # Mensaje de error
        return redirect(url_for('login'))  # Redirigir al login
    return render_template('wiki/magias/magia.html')

@app.route('/wiki/magia/magia_vacia')
def wiki_magia_vacia():
    if 'username' not in session:
        flash('No has iniciado sesión.', 'error')  # Mensaje de error
        return redirect(url_for('login'))  # Redirigir al login
    return render_template('wiki/magias/magia_vacia.html')







@app.route('/wiki/magia/<magia_nombre>')
def wiki_magia_hechizos(magia_nombre):
    if 'username' not in session:
        flash('No has iniciado sesión.', 'error')
        return redirect(url_for('login'))
    print(magia_nombre)
    hechizos = get_hechizos_magia(magia_nombre)  # Obtener hechizos de la magia
    if not hechizos:
        flash(f"No se encontraron hechizos para '{magia_nombre}'.", 'error')
        return redirect(url_for('wiki_magia_vacia'))  # Redirigir a la lista de magias

    return render_template('wiki/magias/magia_hechizos.html', hechizos=hechizos, magia_nombre=magia_nombre)


######################### WIKI PARA RAZAS ###################################
@app.route('/wiki/razas')
def wiki_razas():
    if 'username' not in session:
        flash('No has iniciado sesión.', 'error')  # Mensaje de error
        return redirect(url_for('login'))  # Redirigir al login
    

    return render_template('wiki/razas.html')
#############################################################################


################################### MENU ADMIN ESTADOS ##############################
@app.route("/admin/estados")
def admin_estados():
    if 'username' not in session:
        flash('No has iniciado sesión.', 'error')  # Mensaje de error
        return redirect(url_for('login'))  # Redirigir al login
    
    usuario = obtener_usuario_por_nombre(session['username'])
    
    if not usuario[2]:
        return redirect(url_for('home'))
    
    estados_detalle = {}
    for estado in get_all_estados():
        estados_detalle[estado['nombre']] = {
            'estado': estado['efecto']

        }
            
    return render_template("admin/estados/estados.html", estados=estados_detalle)

@app.route('/admin/borrar_estado/<nombre_estado>', methods=['POST'])
def admin_borrar_estado(nombre_estado):
    if 'username' not in session:
        flash('No has iniciado sesión.', 'error')
        return redirect(url_for('login'))

    usuario = obtener_usuario_por_nombre(session['username'])
    if not usuario[2]:  # Si no es admin
        return redirect(url_for('home'))

    # Verificar si el estado existe antes de eliminarlo
    estado = get_estado(nombre_estado)
    if not estado:
        flash('Estado no encontrado.', 'error')
        return redirect(url_for("admin_estados"))

    # Eliminar el estado de la base de datos
    borrar_estado(nombre_estado)

    flash('Estado eliminado exitosamente.', 'success')
    return redirect(url_for("admin_estados"))

@app.route("/admin/editar_estado/<nombre_estado>", methods=["POST", "GET"])
def admin_editar_estado(nombre_estado):
    if 'username' not in session:
        flash('No has iniciado sesión.', 'error')
        return redirect(url_for('login'))

    usuario = obtener_usuario_por_nombre(session['username'])
    if not usuario[2]:  # Si no es admin
        return redirect(url_for('home'))

    # Obtener el estado a editar
    estado = get_estado(nombre_estado)
    if not estado:
        flash('Estado no encontrado.', 'error')
        return redirect(url_for('admin_estados'))
    
    
    if request.method == 'POST':
        # Recoger los datos del formulario
        datos_estado = {
            'nombre': request.form['nombre'],
            'efecto': request.form['efecto']
        }
        # Modificar el estado en la base de datos
        try:
            modificar_estado(nombre_estado, datos_estado['nombre'], datos_estado['efecto'])
            flash('Estado actualizado exitosamente.', 'success')
        except Exception as e:
            flash(f'Error al actualizar el estado: {str(e)}', 'error')

        return redirect(url_for('admin_estados'))

    # Si es GET, mostrar el formulario con los datos actuales
    return render_template("admin/estados/editar_estado.html", estado=estado)

@app.route("/admin/crear_estado", methods=["POST", "GET"])
def admin_crear_estado():
    if 'username' not in session:
        flash('No has iniciado sesión.', 'error')
        return redirect(url_for('login'))

    usuario = obtener_usuario_por_nombre(session['username'])
    if not usuario[2]:  # Si no es admin
        return redirect(url_for('home'))

    if request.method == "POST":
        # Recoger los datos del formulario
        nombre = request.form['nombre']
        efecto = request.form['efecto']

        # Crear diccionario con los datos
        estado_data = {
            'nombre': nombre,
            'efecto': efecto
        }

        # Guardar en la base de datos
        try:
            agregar_estado(**estado_data)
            flash('Estado creado exitosamente.', 'success')
            return redirect(url_for("admin_estados"))
        except Exception as e:
            flash(f'Error al crear el estado: {str(e)}', 'error')
            return render_template('admin/estados/crear_estado.html', estado=estado_data)

    # Si es GET, mostrar formulario vacío
    return render_template("admin/estados/crear_estado.html")
##################################################################################


################################### MENU ADMIN HABILIDADES ##############################
@app.route("/admin/habilidades")
def admin_habilidades():
    if 'username' not in session:
        flash('No has iniciado sesión.', 'error')
        return redirect(url_for('login'))

    usuario = obtener_usuario_por_nombre(session['username'])
    if not usuario[2]:  # Si no es admin
        return redirect(url_for('home'))

    habilidades_detalle = {}
    for habilidad in get_all_habilidades():
        habilidades_detalle[habilidad['nombre']] = {
            'coste': habilidad['coste'],
            'rango': habilidad['rango'],
            'duracion': habilidad['duracion'],
            'casteo': habilidad['casteo'],
            'descripcion': habilidad['descripcion'],
            'clase': habilidad['clase'],
            'raza': habilidad['raza'],
            'otro': habilidad['otro']
        }

    return render_template("admin/habilidades/habilidades.html", habilidades=habilidades_detalle)

@app.route("/admin/crear_habilidad", methods=["POST", "GET"])
def admin_crear_habilidad():
    if 'username' not in session:
        flash('No has iniciado sesión.', 'error')
        return redirect(url_for('login'))

    usuario = obtener_usuario_por_nombre(session['username'])
    if not usuario[2]:  # Si no es admin
        return redirect(url_for('home'))

    if request.method == "POST":
        # Recoger los datos del formulario de manera segura
        nombre = request.form.get('nombre')
        coste = request.form.get('coste')
        rango = request.form.get('rango')
        duracion = request.form.get('duracion')
        casteo = request.form.get('casteo')
        descripcion = request.form.get('descripcion', '')  # Definir un valor por defecto en caso de que falte
        clase = request.form.get('clase', '')
        raza = request.form.get('raza', '')
        otro = request.form.get('otro', '')

        # Verificar si los campos requeridos no están vacíos
        if not nombre or not coste or not rango:
            flash('Por favor complete todos los campos requeridos.', 'error')
            return render_template('admin/habilidades/crear_habilidad.html')

        # Crear diccionario con los datos
        habilidad_data = {
            'nombre': nombre,
            'coste': coste,
            'rango': rango,
            'duracion': duracion,
            'casteo': casteo,
            'descripcion': descripcion,
            'clase': clase,
            'raza': raza,
            'otro': otro
        }

        # Guardar en la base de datos
        try:
            agregar_habilidad(**habilidad_data)
            flash('Habilidad creada exitosamente.', 'success')
            return redirect(url_for("admin_habilidades"))
        except Exception as e:
            flash(f'Error al crear la habilidad: {str(e)}', 'error')
            print(str(e))
            return render_template('admin/habilidades/crear_habilidad.html', habilidad=habilidad_data)

    # Si es GET, mostrar formulario vacío
    return render_template("admin/habilidades/crear_habilidad.html")


# ✏️ Editar una habilidad
@app.route("/admin/editar_habilidad/<nombre_habilidad>", methods=["POST", "GET"])
def admin_editar_habilidad(nombre_habilidad):
    if 'username' not in session:
        flash('No has iniciado sesión.', 'error')
        return redirect(url_for('login'))

    usuario = obtener_usuario_por_nombre(session['username'])
    if not usuario[2]:  # Si no es admin
        return redirect(url_for('home'))

    # Obtener la habilidad a editar
    habilidad = get_habilidad(nombre_habilidad)
    if not habilidad:
        flash('Habilidad no encontrada.', 'error')
        return redirect(url_for('admin_habilidades'))

    if request.method == 'POST':
        # Recoger los datos del formulario
        datos_habilidad = {
            'nombre': request.form['nombre'],
            'coste': request.form['coste'],
            'rango': request.form['rango'],
            'duracion': request.form['duracion'],
            'casteo': request.form['casteo'],
            'descripcion': request.form['descripcion'],
            'clase': request.form.get('clase', ''),
            'raza': request.form.get('raza', ''),
            'otro': request.form.get('otro', '')
        }

        # Modificar la habilidad en la base de datos
        try:
            modificar_habilidad(nombre_habilidad, **datos_habilidad)
            flash('Habilidad actualizada exitosamente.', 'success')
            return redirect(url_for('admin_habilidades'))
        except Exception as e:
            flash(f'Error al actualizar la habilidad: {str(e)}', 'error')

    # Si es GET, mostrar el formulario con los datos actuales
    return render_template("admin/habilidades/editar_habilidad.html", habilidad=habilidad)

# 🗑️ Eliminar una habilidad
@app.route('/admin/borrar_habilidad/<nombre_habilidad>', methods=['POST'])
def admin_borrar_habilidad(nombre_habilidad):
    if 'username' not in session:
        flash('No has iniciado sesión.', 'error')
        return redirect(url_for('login'))

    usuario = obtener_usuario_por_nombre(session['username'])
    if not usuario[2]:  # Si no es admin
        return redirect(url_for('home'))

    # Verificar si la habilidad existe antes de eliminarla
    habilidad = get_habilidad(nombre_habilidad)
    if not habilidad:
        flash('Habilidad no encontrada.', 'error')
        return redirect(url_for("admin_habilidades"))

    # Eliminar la habilidad de la base de datos
    borrar_habilidad(nombre_habilidad)

    flash('Habilidad eliminada exitosamente.', 'success')
    return redirect(url_for("admin_habilidades"))
##################################################################################


if __name__ == '__main__':
    app.run(debug=True)