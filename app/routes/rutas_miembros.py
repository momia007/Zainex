# ░▒▓ Módulo de rutas para gestionar miembros ▓▒░
# Incluye vistas protegidas para listar, crear y administrar miembros.
# Aplica lógica de visibilidad según el rol del usuario.

from datetime import datetime
import pymysql
from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from app.config import conectar_db
from app.utils.permisos import requiere_rol
from app.utils.current_user import get_contexto_usuario_actual
from flask import redirect, url_for
from app.utils.validar_miembro import validar_datos_miembro

# Creamos el blueprint para miembros
miembros_bp = Blueprint('miembros', __name__)

# ░▒▓ Ruta protegida para listar miembros activos ▓▒░
# Se accede desde el home y muestra todos los miembros activos
# Si el usuario es admin, filtra por su grupo
@miembros_bp.route('/miembros')
@login_required
#@requiere_rol(['admin', 'super_admin'])
def miembros():
    conn = conectar_db()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            if current_user.super_admin:
                # Super admin ve todos los miembros activos, sin filtrar por grupo
                cursor.execute("""
                    SELECT m.*, g.nombre_grupo, f.nombre_funcion
                    FROM miembros m
                    LEFT JOIN grupos g ON m.id_grupo = g.id_grupo
                    LEFT JOIN funciones_miembro fm ON m.id_miembros = fm.id_miembro
                        AND fm.hasta_fecha IS NULL
                    LEFT JOIN funciones f ON fm.id_funcion = f.id_funcion
                    WHERE m.activo_miembros = TRUE
                """)
            else:
                # Admin común ve sólo miembros de su grupo
                cursor.execute("""
                    SELECT m.*, g.nombre_grupo, f.nombre_funcion
                    FROM miembros m
                    LEFT JOIN grupos g ON m.id_grupo = g.id_grupo
                    LEFT JOIN funciones_miembro fm ON m.id_miembros = fm.id_miembro
                        AND fm.hasta_fecha IS NULL
                    LEFT JOIN funciones f ON fm.id_funcion = f.id_funcion
                    WHERE m.id_grupo = %s AND m.activo_miembros = TRUE
                """, (current_user.id_grupo,))

            lista_miembros = cursor.fetchall()
    finally:
        conn.close()


    # Renderiza la vista de miembros con la lista correspondiente
    return render_template('miembros.html', miembros=lista_miembros)

# ░▒▓ Ruta protegida para crear un nuevo miembro ▓▒░
# Se accede desde el formulario de nuevo miembro


@miembros_bp.route('/nvo_miembro')
@login_required
@requiere_rol(['admin', 'super_admin'])
def nvo_miembro():
    con=conectar_db()
    with con.cursor() as cursor:
        cursor.execute("SELECT id_funcion, nombre_funcion FROM funciones")
        funciones = cursor.fetchall()
    con.close()
    mensaje= request.args.get('mensaje')
    campo= request.args.get('campo')
    grupo_info = None
    contexto = get_contexto_usuario_actual()
    return render_template('nvo_miembro.html', funciones=funciones, contexto=contexto, mensaje=mensaje, campo=campo)

# ░▒▓ Ruta para guardar un nuevo miembro ▓▒░
# Recibe datos del formulario y los guarda en la base de datos
# Realiza validaciones básicas y maneja errores comunes
# Redirige a la vista de nuevo miembro con un mensaje de éxito o error
@miembros_bp.route('/guardar_miembro', methods=['POST'])
@login_required
@requiere_rol(['admin', 'super_admin'])
def guardar_miembro():
    # Obtiene los datos del formulario
    # Determina el grupo según el rol del usuario
    if current_user.rol_usuario in ['super_admin']:
        id_grupo = request.form.get('id_grupo')
    else:
        id_grupo = current_user.id_grupo

    dni = request.form.get('dni_miembro')
    apellido = request.form.get('apellido_miembro')
    nombre = request.form.get('nombre_miembro')
    sexo = request.form.get('sexo_miembro')
    fecha_nacimiento = request.form.get('fecha_nac_miembro')
    nacion = request.form.get('nacionalidad_miembro')
    if nacion == 'otro':
        nacionalidad = request.form.get('nacionalidad_otro')
    else:
        nacionalidad = nacion
    religion = request.form.get('religion_miembro')
    estado_civil = request.form.get('estado_civil_miembro')
    codigo = request.form.get('caract_miembro')
    telefono = request.form.get('telefono_miembro')
    num_tel = f"{codigo.strip()} {telefono.strip()}"
    emergencia = request.form.get('emergencia_miembro')
    direccion = request.form.get('direccion_miembro')
    mail = request.form.get('mail_miembro')
    fecha_afil = request.form.get('fecha_afil_miembro')

    # Validación de datos del formulario
    resultado = validar_datos_miembro(request.form)

    # Si hay un error en la validación, redirige con el mensaje de error
    # si el estado es 'error', redirige al formulario con el mensaje
    # si el estado es 'ok', continúa con la inserción en la base de datos
    if resultado['estado'] == 'error':
        return redirect(url_for('miembros.nvo_miembro', mensaje=resultado['mensaje']))
    else:
        conn = conectar_db()
        try:
            print(id_grupo, dni, nombre, apellido, sexo, fecha_nacimiento, nacionalidad,
            religion, estado_civil, num_tel, direccion, emergencia, mail, fecha_afil)
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO miembros (
                        id_grupo, dni_miembros, nombre_miembros, apellido_miembros,
                        sexo_miembros, fecha_nac_miembros, nacionalidad_miembros,
                        religion_miembros, estado_civil_miembros, telefono_miembros,
                        direccion_miembros, emergencia, mail_miembros, fecha_afil_miembros,
                        activo_miembros, creado_en_miembros)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, TRUE, NOW())""",
                        (id_grupo, dni, nombre, apellido, sexo, fecha_nacimiento, nacionalidad,
                        religion, estado_civil, num_tel, direccion, emergencia, mail, fecha_afil))
                id_funcion = request.form.get('funcion_inicial')
                fecha_desde = datetime.today().date()
                id_nuevo_miembro = cursor.lastrowid  # Recupera el ID recién generado

                cursor.execute("""
                    INSERT INTO funciones_miembro (id_miembro, id_funcion, desde_fecha)
                        VALUES (%s, %s, %s)""", (id_nuevo_miembro, id_funcion, fecha_desde))

                conn.commit()
        except pymysql.err.IntegrityError:
            return redirect(url_for('miembros.nvo_miembro', mensaje='DNI ya registrado', campo='dni_miembro'))

        finally:
            conn.close()

    return redirect(url_for('miembros.nvo_miembro', mensaje='ok'))
