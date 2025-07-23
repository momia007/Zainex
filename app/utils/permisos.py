from functools import wraps
from flask import redirect, url_for
from flask_login import current_user

def requiere_rol(roles_permitidos):
    """
    Decorador para proteger rutas según una lista de roles.
    Ejemplo: @requiere_rol(['admin', 'super_admin'])
    """
    def decorador(f):
        @wraps(f)
        def funcion_protegida(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('auth.mostrar_login'))

            # Si se incluye el rol 'super_admin' como permiso
            if 'super_admin' in roles_permitidos and current_user.super_admin:
                return f(*args, **kwargs)

            # Si el rol de usuario coincide
            if current_user.rol_usuario in roles_permitidos:
                return f(*args, **kwargs)

            return "Acceso denegado", 403
        return funcion_protegida
    return decorador
