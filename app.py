from flask import Flask, render_template, request, jsonify, session, redirect, send_from_directory
from flask_socketio import SocketIO, emit
import os
from database import get_db, init_db, close_connection
import bcrypt
from flask_session import Session
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a strong secret key
socketio = SocketIO(app)
# Database initialization
with app.app_context():
    init_db()
@app.teardown_appcontext
def teardown_db(exception):
    close_connection(exception)
# Authentication Route
@app.route('/login', methods=['POST'])
def login():
    db = get_db()
    cursor = db.cursor()
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    # Check if the user exists in the database
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    user = cursor.fetchone()
    if user:
        # Compare the submitted password with the stored hash
        if bcrypt.checkpw(password.encode(), user[2].encode()):
            session['user_id'] = user[0]  # Store user ID in the session
            return jsonify({'message': 'Login successful'}), 200
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
    else:
        return jsonify({'error': 'Invalid credentials'}), 401
    
    
# Registration Route
@app.route('/register', methods=['POST'])
def register():
    db = get_db()
    cursor = db.cursor()
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    # Check if the username already exists
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    user = cursor.fetchone()
    if user:
        return jsonify({'error': 'Username already exists'}), 400
    # Hash the password
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    # Add the user to the database
    cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, 'user')", (username, password_hash))
    db.commit()
    return jsonify({'message': 'User registered successfully'}), 201
# Redirect to Login Page (If not authenticated)
@app.before_request
def require_login():
    if 'user_id' not in session and request.endpoint in ['index', 'principal', 'fichas', 'mapas', 'wiki']:
        return redirect('/login')
# Serve static files
@app.route('/')
def index():
    if 'user_id' in session:
        with app.app_context():
            db = get_db()
            cursor = db.cursor()
            cursor.execute("SELECT username FROM users WHERE id = ?", (session['user_id'],))
            user = cursor.fetchone()
            username = user[0] if user else 'User'
            print(f"Username: {username}")  # Debugging line
        return render_template('index.html', username=username)
    else:
        return redirect('/login')


@app.route('/principal.html')
def principal():
    if 'user_id' in session:
        with app.app_context():
            db = get_db()
            cursor = db.cursor()
            cursor.execute("SELECT username FROM users WHERE id = ?", (session['user_id'],))
            user = cursor.fetchone()
            username = user[0] if user else 'User'
            print(f"Username: {username}")  # Debugging line
        return render_template('principal.html', username=username)
    else:
        return jsonify({'error': 'Not authenticated'}), 401
# Fichas Page (Protected)

@app.route('/fichas.html')
def fichas():
    if 'user_id' in session:
        with app.app_context():
            db = get_db()
            cursor = db.cursor()
            cursor.execute("SELECT * FROM pdfs")
            pdfs = cursor.fetchall() 
            cursor.execute("SELECT username, role FROM users WHERE id = ?", (session['user_id'],))
            user = cursor.fetchone()
            username = user[0] if user else 'User'
            role = user[1] if user else "usuario"
        return render_template('fichas.html', pdfs=pdfs, username=username, role=role)  # Pass pdfs to the template
    else:
        return jsonify({'error': 'Not authenticated'}), 401
    
    

    if 'user_id' in session:
        return render_template('wiki.html')
    else:
        return jsonify({'error': 'Not authenticated'}), 401
# Upload PDF Route
@app.route('/upload', methods=['POST'])
def upload_pdf():
    if 'user_id' in session:  # Check if the user is logged in        
        file = request.files['pdf_file']  # Assuming the file input has the name 'pdf_file'
        if file:
            db = get_db()
            cursor = db.cursor()
            cursor.execute("SELECT username FROM users WHERE id = ?", (session['user_id'],))
            user = cursor.fetchone()
            username = user[0] if user else 'User'
            filename = username+"_"+file.filename
            pdf_folder = os.path.join('static', 'pdf')
            filepath = os.path.join(pdf_folder, filename)
            # Make sure the static/pdf folder exists
            if not os.path.exists(pdf_folder):
                os.makedirs(pdf_folder)
            # Save the file
            file.save(filepath)
            # Store the file information in the database (including the owner_id)
            with app.app_context():
                db = get_db()
                cursor = db.cursor()
                cursor.execute("SELECT username FROM users WHERE id = ?", (session['user_id'],))
                user = cursor.fetchone()
                username = user[0] if user else 'User'
                cursor.execute("INSERT INTO pdfs (filename, owner) VALUES (?, ?)", (filename, username))
                db.commit()
                return jsonify({'message': 'PDF uploaded successfully'}), 200
        else:
            return jsonify({'error': 'No file uploaded'}), 400
    else:
        return jsonify({'error': 'Not authenticated'}), 401
    
    
@app.route('/pdf/<filename>')
def view_pdf(filename):
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT filename FROM pdfs WHERE filename = ?", (filename,))
        pdf = cursor.fetchone()
        
        if pdf:
            # Path to the folder where PDFs are stored
            pdf_folder = os.path.join('static', 'pdf')
            # Return the PDF file from the static directory
            return send_from_directory(pdf_folder, pdf[0])
        else:
            return jsonify({'error': 'PDF not found'}), 404
    
    
@app.route('/delete_pdf/<pdf_id>', methods=['POST'])
def delete_pdf(pdf_id):
    if 'user_id' in session:
        with app.app_context():
            db = get_db()
            cursor = db.cursor()
            # Obtener información del usuario
            cursor.execute("SELECT username, role FROM users WHERE id = ?", (session['user_id'],))
            user = cursor.fetchone()
            username = user[0]
            role = user[1]
            
            # Obtener el PDF a eliminar
            cursor.execute("SELECT filename, owner FROM pdfs WHERE id = ?", (pdf_id,))
            pdf = cursor.fetchone()

            if pdf:
                filename, owner = pdf

                # Verificar si el usuario es el dueño o tiene el rol de admin
                if owner == username or role == 'admin':
                    # Eliminar el archivo del sistema de archivos
                    pdf_folder = os.path.join('static', 'pdf')
                    filepath = os.path.join(pdf_folder, filename)
                    if os.path.exists(filepath):
                        os.remove(filepath)
                    
                    # Eliminar el registro de la base de datos
                    cursor.execute("DELETE FROM pdfs WHERE id = ?", (pdf_id,))
                    db.commit()

                    return jsonify({'message': 'PDF deleted successfully'}), 200
                else:
                    return jsonify({'error': 'Unauthorized action'}), 403
            else:
                return jsonify({'error': 'PDF not found'}), 404
    else:
        return jsonify({'error': 'Not authenticated'}), 401
    
    
if __name__ == '__main__':
    socketio.run(app, debug=True)