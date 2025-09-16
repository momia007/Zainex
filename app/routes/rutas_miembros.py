# ░▒▓ Módulo de rutas para gestionar miembros ▓▒░
# Incluye vistas protegidas para listar, crear y administrar miembros.
# Aplica lógica de visibilidad según el rol del usuario.

from datetime import datetime
from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from app.utils.permisos import requiere_rol
from app.utils.current_user import get_contexto_usuario_actual
from flask import redirect, url_for
from app.utils.validar_miembro import validar_datos_miembro

from app.models.miembro import Miembro
from app.models.grupo import Grupo
from app.models.funcion import Funcion
from app.models.funciones_miembro import FuncionMiembro
from sqlalchemy.orm import joinedload
from app.extensions import db


# Creamos el blueprint para miembros
miembros_bp = Blueprint('miembros', __name__)

# ░▒▓ Ruta protegida para listar miembros activos ▓▒░
# Se accede desde el home y muestra todos los miembros activos
# Si el usuario es admin, filtra por su grupo
@miembros_bp.route('/miembros')
@login_required
def miembros():
    if current_user.super_admin:
        miembros = (
            Miembro.query
            .filter_by(activo_miembros=True)
            .options(
                joinedload(Miembro.grupo),
                joinedload(Miembro.funciones_actuales).joinedload(FuncionMiembro.funcion)
            )
            .all()
        )
    else:
        miembros = (
            Miembro.query
            .filter_by(activo_miembros=True, id_grupo=current_user.id_grupo)
            .options(
                joinedload(Miembro.grupo),
                joinedload(Miembro.funciones_actuales).joinedload(FuncionMiembro.funcion)
            )
            .all()
        )

    return render_template('miembros.html', miembros=miembros)


# ░▒▓ Ruta para guardar un nuevo miembro ▓▒░
# Recibe datos del formulario y los guarda en la base de datos
# Realiza validaciones básicas y maneja errores comunes
# Redirige a la vista de nuevo miembro con un mensaje de éxito o error


@miembros_bp.route('/guardar_miembro', methods=['POST'])
@login_required
@requiere_rol(['admin', 'super_admin'])
def guardar_miembro():
    id_grupo = request.form.get('id_grupo') if current_user.rol_usuario == 'super_admin' else current_user.id_grupo
    datos = request.form
    nacionalidad = datos.get('nacionalidad_otro') if datos.get('nacionalidad_miembro') == 'otro' else datos.get('nacionalidad_miembro')
    num_tel = f"{datos.get('caract_miembro').strip()} {datos.get('telefono_miembro').strip()}"

    resultado = validar_datos_miembro(datos)
    if resultado['estado'] == 'error':
        return redirect(url_for('miembros.nvo_miembro', mensaje=resultado['mensaje']))

    try:
        nuevo = Miembro(
            id_grupo=id_grupo,
            dni_miembros=datos.get('dni_miembro'),
            nombre_miembros=datos.get('nombre_miembro'),
            apellido_miembros=datos.get('apellido_miembro'),
            sexo_miembros=datos.get('sexo_miembro'),
            fecha_nac_miembros=datos.get('fecha_nac_miembro'),
            nacionalidad_miembros=nacionalidad,
            religion_miembros=datos.get('religion_miembro'),
            estado_civil_miembros=datos.get('estado_civil_miembro'),
            telefono_miembros=num_tel,
            direccion_miembros=datos.get('direccion_miembro'),
            emergencia=datos.get('emergencia_miembro'),
            mail_miembros=datos.get('mail_miembro'),
            fecha_afil_miembros=datos.get('fecha_afil_miembro'),
            activo_miembros=True,
            creado_en_miembros=datetime.now()
        )
        db.session.add(nuevo)
        db.session.flush()  # Para obtener el ID antes del commit

        funcion_inicial = FuncionMiembro(
            id_miembro=nuevo.id_miembros,
            id_funcion=datos.get('funcion_inicial'),
            desde_fecha=datetime.today().date()
        )
        db.session.add(funcion_inicial)
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        if 'duplicate key' in str(e).lower():
            return redirect(url_for('miembros.nvo_miembro', mensaje='DNI ya registrado', campo='dni_miembro'))
        else:
            raise e

    return redirect(url_for('miembros.nvo_miembro', mensaje='ok'))
