from flask import Blueprint, request, jsonify, render_template, redirect, url_for
import pymysql
import bcrypt
from app.config import conectar_db  # Asegurate de que esta función exista
from flask_login import login_user, logout_user
from app.models.usuario import Usuario  # Asegurate de que este modelo exista


auth_bp = Blueprint('auth', __name__)

# Vista principal que muestra el formulario de login web


@auth_bp.route('/')
def mostrar_login():
    return render_template('login.html')


# Ruta para manejar el inicio de sesión
@auth_bp.route('/login', methods=['POST'])
def login():
    datos = request.get_json()  # 👈 importante: usar get_json()
    dni = datos.get('dni')
    contrasena = datos.get('contrasena')

    if not dni or not contrasena:
        return jsonify({'mensaje': 'DNI y contraseña son obligatorios'}), 400

    conn = conectar_db()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(
                "SELECT * FROM usuarios WHERE dni_usuario = %s AND estado_usuario = TRUE",(dni,)
            )
            usuario = cursor.fetchone()
        
        if usuario and bcrypt.checkpw(contrasena.encode(), usuario['pass_usuario_hash'].encode()):
            # Si las credenciales son válidas, creamos el objeto Usuario
            
            # Verificamos si es super admin, si es 1 = true, de lo contrario es false
            es_super_admin = usuario['super_admin'] == 1

            usuario_obj = Usuario(
            id=usuario['id_usuarios'],
            dni=usuario['dni_usuario'],
            nombre=usuario['nombre_usuario'],
            rol=usuario['rol_usuario'],
            super_admin=es_super_admin,
            id_grupo=usuario['id_grupo'],
            )
            
            # Iniciamos sesión con el usuario
            login_user(usuario_obj)

            # Redirigimos al inicio o a la página de inicio
            return jsonify({'mensaje': 'OK'}), 200
            #return redirect('/home')
        else:
            return jsonify({'mensaje': 'DNI o contraseña incorrecta'}), 401

    finally:
        conn.close()
        
# Ruta para manejar el cierre de sesión
@auth_bp.route('/logout')
def logout():
    logout_user();  # Elimina el usuario de la sesión
    return redirect('/')

