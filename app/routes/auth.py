from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import login_user, logout_user
from app.models.usuario import Usuario


auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def mostrar_login():
    return render_template('login.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    mensaje_error = None
    if request.method == 'POST':
        dni = request.form.get('dni')
        contrasena = request.form.get('contrasena')

        usuario = Usuario.query.filter_by(dni_usuario=dni, estado_usuario=True).first()

        if not usuario:
            mensaje_error = "⚠️ Usuario no encontrado o inactivo."
        elif not usuario.verificar_contrasena(contrasena):
            mensaje_error = "🔒 Contraseña incorrecta."
        else:
            login_user(usuario)
            return redirect(url_for('admin.home'))

    return render_template('login.html', mensaje_error=mensaje_error)


@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect('/')


