from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_login import login_required, current_user
from datetime import datetime
from app.extensions import db
from app.models.usuario import Usuario
from app.models.grupo import Grupo
from app.models.funcion import Funcion
from app.models.funciones_miembro import FuncionMiembro
from app.utils.seguridad import hash_clave

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/home')
@login_required
def home():
    return render_template('home.html')


@admin_bp.route('/usuarios')
@login_required
def usuarios():
    if current_user.super_admin:
        usuarios_en_vista = Usuario.query.outerjoin(Grupo).add_columns(
            Usuario.id_usuario,
            Usuario.nombre_usuario,
            Usuario.apellido_usuario,
            Usuario.dni_usuario,
            Usuario.rol_usuario,
            Grupo.nombre_grupo
        ).all()
    else:
        usuarios_en_vista = Usuario.query.filter_by(id_grupo=current_user.id_grupo).outerjoin(Grupo).add_columns(
            Usuario.id_usuario,
            Usuario.nombre_usuario,
            Usuario.apellido_usuario,
            Usuario.dni_usuario,
            Usuario.rol_usuario,
            Grupo.nombre_grupo
        ).all()
    return render_template('usuarios.html', usuarios=usuarios_en_vista)

@admin_bp.route('/nvo_usuario')
@login_required
def nvo_usuario():
    grupos = Grupo.query.all()
    return render_template('nvo_usuario.html', grupos=grupos)

@admin_bp.route('/guardar_usuario', methods=['POST'])
@login_required
def guardar_usuario():
    id_grupo = request.form['grupo']
    dni = request.form['dni']
    clave = request.form['clave']
    rol_usuario = request.form['rol']
    nombre = request.form['nombre']
    apellido = request.form['apellido']

    hash_pass = hash_clave(clave)

    nuevo_usuario = Usuario(
        id_grupo=id_grupo,
        dni_usuario=dni,
        pass_usuario_hash=hash_pass,
        rol_usuario=rol_usuario,
        nombre_usuario=nombre,
        apellido_usuario=apellido,
        creado_en_usuario=datetime.now()
    )
    db.session.add(nuevo_usuario)
    db.session.commit()

    return redirect(url_for('admin.usuarios'))

@admin_bp.route('/funciones')
@login_required
def funciones():
    funciones = Funcion.query.all()
    return render_template('funciones.html', funciones=funciones)

@admin_bp.route('/nva_funcion')
@login_required
def nva_funcion():
    return render_template('nva_funcion.html')

@admin_bp.route('/agregar_funcion', methods=['POST'])
@login_required
def agregar_funcion():
    nombre = request.form['nombre']
    abreviacion = request.form['abreviacion']
    descripcion = request.form['descripcion']

    nueva_funcion = Funcion(
        nombre_funcion=nombre,
        abrev_funcion=abreviacion,
        descripcion=descripcion
    )
    db.session.add(nueva_funcion)
    db.session.commit()

    return redirect(url_for('admin.funciones'))

@admin_bp.route('/grupos')
@login_required
def grupos():
    grupos = Grupo.query.all()
    return render_template('grupos.html', grupos=grupos)

@admin_bp.route('/nvo_grupo')
@login_required
def nvo_grupo():
    return render_template('nvo_grupo.html')

@admin_bp.route('/existe_grupo', methods=['POST'])
@login_required
def existe_grupo():
    num = request.form['numero']
    existe = Grupo.query.filter_by(num_grupo=num).count() > 0
    return jsonify({"existe": existe})

@admin_bp.route('/guardar_grupo', methods=['POST'])
@login_required
def guardar_grupo():
    nombre = request.form['nombre']
    numero = request.form['numero']
    distrito = request.form['distrito']
    zona = request.form['zona']

    nuevo_grupo = Grupo(
        nombre_grupo=nombre,
        num_grupo=numero,
        distrito_grupo=distrito,
        zona_grupo=zona,
        creado_en_grupo=datetime.now()
    )
    db.session.add(nuevo_grupo)
    db.session.commit()

    return redirect(url_for('admin.grupos'))
