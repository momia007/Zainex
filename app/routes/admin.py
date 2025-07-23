# Módulo de rutas protegidas para administradores.
# Incluye vistas para mostrar el formulario de carga de funciones
# y para insertar nuevas funciones en la base de datos.
# Todas las rutas exigen que el usuario esté logueado y tenga rol administrativo.

from flask import Blueprint, request, jsonify, render_template
# Importamos el decorador que exige login y el usuario actual
from flask_login import login_required, current_user
# Asegurate de que esta función exista y devuelva la conexión a MySQL
from app.config import conectar_db
# Importamos funciones para renderizar templates HTML
from flask import render_template
# Importamos permisos.py para verificar roles
from app.utils.permisos import requiere_rol
# Importamos pymysql para manejar la conexión a MySQL
import pymysql
# Importamos la función para generar y verificar contraseñas
import bcrypt
# Importamos la función que convierte códigos de mensaje a texto legible
from app.utils.mensajes import mensaje_legible

admin_bp = Blueprint('admin', __name__)

#---------------
#     Rutas
#---------------

# Esta ruta se encarga de mostrar la página home
@admin_bp.route('/home')
@login_required  # Esta ruta solo se puede acceder si hay sesión activa
def home():
    # Renderizamos la vista home.html y le pasamos el usuario actual
    return render_template('home.html', usuario=current_user)

# Vista protegida para mostrar el formulario de carga de funciones Solo Super Admin
@admin_bp.route('/nva_funcion')
@login_required
@requiere_rol('super_admin')  # Solo super_admin puede acceder
def nva_funcion():
    return render_template('nva_funcion.html')

# ░▒▓ Ruta que muestra el formulario para crear un nuevo usuario ▓▒░
# Esta función se ejecuta cuando se accede a /nvo_usuario
# Verifica el tipo de usuario logueado (admin o super_admin)
# Si es admin, carga automáticamente los datos del grupo desde la base
# Si es super_admin, deja los campos para que se completen manualmente
@admin_bp.route('/nvo_usuario')
@login_required
@requiere_rol(['admin','super_admin'])  # Restringimos el acceso según rol
def nvo_usuario():
    # Inicializamos variables para que siempre existan, incluso si no se llenan
    nombre_grupo = ''
    num_grupo = ''

    # Si el usuario es un admin (no puede elegir grupo), se lo asignamos automáticamente
    if not current_user.super_admin:
        conn = conectar_db()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                # Consultamos nombre y número de grupo según el id del usuario
                cursor.execute("""
                    SELECT nombre_grupo, num_grupo
                    FROM grupos
                    WHERE id_grupo = %s
                """, (current_user.id_grupo,))
                grupo = cursor.fetchone()

                # Si encontramos el grupo, lo asignamos a las variables
                if grupo:
                    nombre_grupo = grupo['nombre_grupo']
                    num_grupo = grupo['num_grupo']
        finally:
            conn.close()

    # Renderizamos la plantilla HTML, enviando nombre y número de grupo si existen
    return render_template('nvo_usuario.html',
                           nombre_grupo=nombre_grupo,
                           num_grupo=num_grupo)

# ░▒▓ Ruta que muestra el formulario para crear un nuevo usuario ▓▒░
# Esta función se ejecuta cuando se accede a /nvo_usuario
# Verifica el tipo de usuario logueado (admin o super_admin)
# Si es admin, carga automáticamente los datos del grupo desde la base
# Si es super_admin, deja los campos para que se completen manualmente

'''@admin_bp.route('/nvo_miembro')
@login_required
@requiere_rol(['admin','super_admin'])  # Restringimos el acceso según rol
def nvo_miembro():
    # Inicializamos variables para que siempre existan, incluso si no se llenan
    nombre_grupo = ''
    num_grupo = ''

    # Si el usuario es un admin (no puede elegir grupo), se lo asignamos automáticamente
    if not current_user.super_admin:
        conn = conectar_db()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                # Consultamos nombre y número de grupo según el id del usuario
                cursor.execute("""
                    SELECT nombre_grupo, num_grupo
                    FROM grupos
                    WHERE id_grupo = %s
                """, (current_user.id_grupo,))
                grupo = cursor.fetchone()

                # Si encontramos el grupo, lo asignamos a las variables
                if grupo:
                    nombre_grupo = grupo['nombre_grupo']
                    num_grupo = grupo['num_grupo']
        finally:
            conn.close()

    # Renderizamos la plantilla HTML, enviando nombre y número de grupo si existen
    return render_template('nvo_miembro.html',
                           nombre_grupo=nombre_grupo,
                           num_grupo=num_grupo)
'''

# Ruta para manejar nuevos grupos
@admin_bp.route('/nvo_grupo')
@login_required
@requiere_rol(['admin','super_admin'])  # o 'super_admin' si querés restringirlo más
def nvo_grupo():
    return render_template('nvo_grupo.html')

# Ruta para manejar usuarios
@admin_bp.route('/usuarios')
@login_required
def usuarios():
    conn = conectar_db()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            # Detectar rol y grupo
            grupo_usuario = current_user.id_grupo
            rol = current_user.rol_usuario

            # Lógica SQL según rol
            if current_user.super_admin:
                query = """
                    SELECT u.*, g.nombre_grupo AS grupo_nombre
                    FROM usuarios u
                    LEFT JOIN grupos g ON u.id_grupo = g.id_grupo
                """
                cursor.execute(query)
            else:
                query = """
                    SELECT u.*, g.nombre_grupo AS grupo_nombre
                    FROM usuarios u
                    LEFT JOIN grupos g ON u.id_grupo = g.id_grupo
                    WHERE u.id_grupo = %s
                """
                cursor.execute(query, (grupo_usuario,))
            
            usuarios_en_vista = cursor.fetchall()
    finally:
        conn.close()

    return render_template('usuarios.html', lista_usuarios=usuarios_en_vista)
       


#--------------------------------
#   Funciones de la base de datos
#--------------------------------


# Endpoint protegido para procesar el formulario y agregar una nueva función
@admin_bp.route('/agregar_funcion', methods=['POST'])
@login_required
@requiere_rol('super_admin')  # Solo super_admin puede acceder
def agregar_funcion():
    print("📥 Se recibió un POST en /agregar_funcion")  # 👈 Esto imprimirá 

    nombre = request.form.get('nombre')
    abreviacion = request.form.get('abreviacion')
    descripcion = request.form.get('descripcion', '')

    if not nombre:
        return jsonify({'mensaje': 'El nombre de la función es obligatorio'}), 400
    if not abreviacion:
        return jsonify({'mensaje': 'La abreviación es obligatoria'}), 400
    if len(abreviacion) > 3:
        return jsonify({'mensaje': 'La abreviación no puede exceder los 3 caracteres'}), 400
    # Insertar en base de datos
    conn = conectar_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO funciones (nombre_funcion, abrev_funcion, descripcion) VALUES (%s, %s, %s)",
                (nombre, abreviacion, descripcion)
            )
        conn.commit()
        return render_template('nva_funcion.html', mensaje='ok')
        # return jsonify({'mensaje': 'Función creada correctamente'}), 200
    except Exception as e:
        print(f"Error al guardar función: {e}")
        return "Error interno", 500
    finally:
        conn.close()

# Ruta para obtener el nombre de un grupo por su número
# Esta ruta recibe el número de grupo y devuelve el nombre del grupo correspondiente.
# Devuelve un JSON con el nombre del grupo o None si no existe.        
@admin_bp.route('/grupo_nombre/<int:num_grupo>')
@login_required
@requiere_rol(['super_admin'])
def grupo_nombre(num_grupo):
    conn = conectar_db()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("SELECT nombre_grupo FROM grupos WHERE num_grupo = %s", (num_grupo,))
            grupo = cursor.fetchone()
            return jsonify({"nombre": grupo["nombre_grupo"] if grupo else None})
    finally:
        conn.close()
        
# Ruta para verificar si un grupo ya existe
# Esta ruta recibe el nombre del grupo y verifica si ya existe en la base de datos.
# Devuelve un JSON con el resultado de la verificación.
# Si el grupo existe, devuelve {"existe": true}, de lo contrario {"existe": false}.
@admin_bp.route('/existe_grupo/<int:num>')
@login_required
@requiere_rol(['admin', 'super_admin'])
def existe_grupo(num):
    conn = conectar_db()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("SELECT COUNT(*) AS cantidad FROM grupos WHERE num_grupo = %s", (num,))
            resultado = cursor.fetchone()
            return jsonify({"existe": resultado["cantidad"] > 0})
    finally:
        conn.close()
        
# Ruta para guardar un nuevo grupo
# Esta ruta recibe los datos del formulario de creación de grupo y los guarda en la base de datos.
# Realiza validaciones básicas y devuelve un mensaje de éxito o error según corresponda.
# Si el grupo ya existe, devuelve un mensaje de error.
# Si los datos son válidos, guarda el grupo y devuelve un mensaje de éxito.
# Si hay algún error en la conexión a la base de datos, devuelve un mensaje de error.       
@admin_bp.route('/guardar_grupo', methods=['POST'])
@login_required
@requiere_rol(['super_admin'])
def guardar_grupo():
    # Capturamos todos los campos con defaults seguros
    numero = request.form.get('numero', '').strip()
    nombre = request.form.get('nombre', '').strip()
    distrito = request.form.get('distrito', '').strip()
    zona = request.form.get('zona', '').strip()

    # Validaciones generales
    if not numero or not numero.isdigit():
        return render_template('nvo_grupo.html', mensaje='numero_invalido')
    if len(numero) > 6:
        return render_template('nvo_grupo.html', mensaje='numero_largo')

    if not nombre:
        return render_template('nvo_grupo.html', mensaje='nombre_vacio')

    if not distrito or not distrito.isdigit():
        return render_template('nvo_grupo.html', mensaje='distrito_invalido')
    if len(distrito) > 6:
        return render_template('nvo_grupo.html', mensaje='distrito_largo')

    if not zona or not zona.isdigit():
        return render_template('nvo_grupo.html', mensaje='zona_invalida')
    if len(zona) > 6:
        return render_template('nvo_grupo.html', mensaje='zona_larga')

    # Verificamos existencia por número de grupo
    conn = conectar_db()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(
                "SELECT COUNT(*) AS cantidad FROM grupos WHERE num_grupo = %s", (numero,)
            )
            if cursor.fetchone()['cantidad'] > 0:
                return render_template('nvo_grupo.html', mensaje='grupo_duplicado')

            # Si no existe, insertamos
            cursor.execute("""
                INSERT INTO grupos (
                    nombre_grupo, num_grupo, distrito_grupo, zona_grupo, creado_en_grupo
                ) VALUES (%s, %s, %s, %s, NOW())
            """, (nombre, numero, distrito, zona))

            conn.commit()
            return render_template('nvo_grupo.html', mensaje='ok')
    finally:
        conn.close()

# Ruta para guardar un nuevo usuario
# Esta recibe los datos del formulario de creación de usuario y los guarda en la base de datos.
# Realiza validaciones básicas y devuelve un mensaje de éxito o error según corresponda.
@admin_bp.route('/guardar_usuario', methods=['POST'])
@login_required
@requiere_rol(['admin', 'super_admin'])
def guardar_usuario():
    # Activamos modo debug para desarrollo (poner en False en producción)
    DEBUG_MODE = True

    # Si está activado, mostramos todos los datos que llegan del formulario
    if DEBUG_MODE:
        print("🟡 [DEBUG] Datos del formulario:", request.form)

    # ░▒▓ Captura de campos desde el formulario ▓▒░
    # Capturamos el grupo según el tipo de usuario
    if current_user.super_admin:
        # El super_admin escribe manualmente el num_grupo
        num_grupo = request.form.get('num_grupo', '').strip()
        id_grupo = num_grupo  # Se traduce más abajo vía SELECT
    else:
        # El admin pertenece a un grupo fijo (asociado al usuario logueado)
        id_grupo = str(current_user.id_grupo)
        num_grupo = request.form.get('num_grupo','').strip()
  
    # Datos comunes (presentes para todos)
    nombre_grupo = request.form.get('nombre_grupo', '').strip()
    nombre = request.form.get('nombre', '').strip()
    apellido = request.form.get('apellido', '').strip()
    dni = request.form.get('dni_usuario', '').strip()
    password = request.form.get('password', '').strip()
    password2 = request.form.get('re_password', '').strip()
    rol_usuario = request.form.get('rol', '').strip()

    # ░▒▓ Validaciones previas antes de guardar ▓▒░
    if not nombre:
        return render_template('nvo_usuario.html', mensaje='nombre_vacio', num_grupo=num_grupo, nombre_grupo=nombre_grupo)
    if len(nombre) > 100:
        return render_template('nvo_usuario.html', mensaje='nombre_largo', num_grupo=num_grupo, nombre_grupo=nombre_grupo)
    if not apellido:
        return render_template('nvo_usuario.html', mensaje='apellido_vacio', num_grupo=num_grupo, nombre_grupo=nombre_grupo)
    if len(apellido) > 100:
        return render_template('nvo_usuario.html', mensaje='apellido_largo', num_grupo=num_grupo, nombre_grupo=nombre_grupo)
    if not password or len(password) < 6:
        return render_template('nvo_usuario.html', mensaje='password_invalido', num_grupo=num_grupo, nombre_grupo=nombre_grupo)
    if password != password2:
        return render_template('nvo_usuario.html', mensaje='password_no_coincide', num_grupo=num_grupo, nombre_grupo=nombre_grupo)
    if not id_grupo or not id_grupo.isdigit():
        return render_template('nvo_usuario.html', mensaje='grupo_invalido', num_grupo=num_grupo, nombre_grupo=nombre_grupo)
    if (current_user.rol_usuario) not in ['admin', 'super_admin']:
        return render_template('nvo_usuario.html', mensaje='rol_invalido', num_grupo=num_grupo, nombre_grupo=nombre_grupo)
    if rol_usuario == "":
        return render_template('nvo_usuario.html', mensaje='rol_vacio', num_grupo=num_grupo, nombre_grupo=nombre_grupo)

    # ░▒▓ Cifrado de contraseña ▓▒░
    # Solo después de confirmar que password es válido y coincide
    clave = password
    hash_clave = bcrypt.hashpw(clave.encode(), bcrypt.gensalt()).decode('utf-8')

    # Mostramos los datos que se van a insertar en la base (solo si debug está activo)
    if DEBUG_MODE:
        print("🟢 [DEBUG] Datos para la base:", id_grupo, dni, hash_clave, rol_usuario, nombre, apellido)

    # ░▒▓ Operaciones en la base de datos ▓▒░
    conn = conectar_db()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            # Validamos que el DNI no esté duplicado
            cursor.execute("SELECT COUNT(*) AS cantidad FROM usuarios WHERE dni_usuario = %s", (dni,))
            if cursor.fetchone()['cantidad'] > 0:
                return render_template('nvo_usuario.html', mensaje='usuario_duplicado', num_grupo=num_grupo, nombre_grupo=nombre_grupo)

            if current_user.super_admin:
                cursor.execute("SELECT id_grupo FROM grupos WHERE num_grupo = %s", (id_grupo,))
                grupo = cursor.fetchone()
                if not grupo:
                    return render_template('nvo_usuario.html', mensaje='grupo_invalido', num_grupo=num_grupo, nombre_grupo=nombre_grupo)
                id_grupo = grupo['id_grupo']  # Asignamos el id válido


            # Insertamos el nuevo usuario
            print("🟢 [DEBUG] Insertando usuario en la base de datos...")
            print("🟢 [DEBUG] Datos para la base:", id_grupo, dni, hash_clave, rol_usuario, nombre, apellido)
            cursor.execute("""
                INSERT INTO usuarios (
                    id_grupo, dni_usuario, pass_usuario_hash, rol_usuario, nombre_usuario, apellido_usuario, creado_en_usuario
                ) VALUES (%s, %s, %s, %s, %s, %s, NOW())
            """, (id_grupo, dni, hash_clave, rol_usuario, nombre, apellido))
            conn.commit()

            # Mensaje de éxito al usuario
            return render_template('nvo_usuario.html', mensaje='ok')
    finally:
        conn.close()
