# ░▒▓ utils/current_user.py ▓▒░
from flask_login import current_user
from app.models.usuario import Usuario
from app.models.grupo import Grupo

def get_contexto_usuario_actual():
    if current_user.rol_usuario not in ['admin', 'colaborador']:
        return None

    usuario = Usuario.query.filter_by(id_usuario=current_user.id_usuario).join(Grupo).add_columns(
        Usuario.id_usuario,
        Usuario.nombre_usuario,
        Usuario.apellido_usuario,
        Usuario.dni_usuario,
        Usuario.rol_usuario,
        Grupo.id_grupo,
        Grupo.num_grupo,
        Grupo.nombre_grupo
    ).first()

    if usuario:
        return {
            "id_usuario": usuario.id_usuario,
            "nombre_usuario": usuario.nombre_usuario,
            "apellido_usuario": usuario.apellido_usuario,
            "dni_usuario": usuario.dni_usuario,
            "rol_usuario": usuario.rol_usuario,
            "id_grupo": usuario.id_grupo,
            "num_grupo": usuario.num_grupo,
            "nombre_grupo": usuario.nombre_grupo
        }

    return None
