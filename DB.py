import sqlite3
import hashlib
from flask import Flask, request, redirect, render_template_string

# Configuración de Flask
app = Flask(__name__)
PORT = 5800
DB_NAME = "usuarios.db"

# ===============================
# FUNCIONES BASE DE DATOS Y HASH
# ===============================

def crear_tabla():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE,
            hash TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def obtener_hash(texto):
    return hashlib.sha256(texto.encode()).hexdigest()

def insertar_usuario(nombre, contrasena):
    hash_contraseña = obtener_hash(contrasena)
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO usuarios (nombre, hash) VALUES (?, ?)", (nombre, hash_contraseña))
        conn.commit()
    except sqlite3.IntegrityError:
        pass  # Ya existe el usuario
    finally:
        conn.close()

def validar_usuario(nombre, contrasena):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT hash FROM usuarios WHERE nombre = ?", (nombre,))
    fila = cursor.fetchone()
    conn.close()
    if fila:
        return obtener_hash(contrasena) == fila[0]
    return False

# =======================
# RUTAS FLASK (HTML SIMPLE)
# =======================

HTML_FORM = '''
<h2>Login de Usuarios</h2>
<form method="post">
  Usuario: <input name="usuario" required><br>
  Contraseña: <input name="contrasena" type="password" required><br>
  <input type="submit" value="Ingresar">
</form>
<p>{{ mensaje }}</p>
'''

@app.route('/', methods=['GET', 'POST'])
def login():
    mensaje = ""
    if request.method == 'POST':
        usuario = request.form['usuario']
        contrasena = request.form['contrasena']
        if validar_usuario(usuario, contrasena):
            mensaje = f"✅ Bienvenido, {usuario}."
        else:
            mensaje = "❌ Usuario o contraseña incorrectos."
    return render_template_string(HTML_FORM, mensaje=mensaje)

# ===========================
# EJECUTAR EL SITIO EN PUERTO 5800
# ===========================

if __name__ == '__main__':
    crear_tabla()

    # Agregar integrantes del grupo (editables para el examen)
    insertar_usuario("Gabriel", "clave123")
    insertar_usuario("Felipe", "otraClave123")
    insertar_usuario("Valentina", "segura456")

    print(f"Servidor iniciado en http://localhost:{PORT}")
    app.run(port=PORT)
