# app/utils/validar_miembro.py

# ░▒▓ Validaciones del formulario de nuevo miembro ▓▒░

from datetime import datetime
import re
#import datetime

# ░▒▓ Función para calcular la edad a partir de la fecha de nacimiento ▓▒░
def calcular_edad(fecha_nac_str):
    try:
        print(fecha_nac_str)
        fecha_nac = datetime.strptime(fecha_nac_str, '%Y-%m-%d')
        hoy = datetime.today().date()
        edad = hoy.year - fecha_nac.year - ((hoy.month, hoy.day) < (fecha_nac.month, fecha_nac.day))
        print(f"Edad calculada1: {edad}")
        return edad
    except:
        return None


# ░▒▓ Función principal ▓▒░
def validar_datos_miembro(datos_form):
    """
    Recibe el diccionario de datos del formulario enviado por POST.
    Devuelve un dict: {estado: 'ok' | 'error', mensaje: '...' }
    """
    edad = calcular_edad(datos_form.get('fecha_nac_miembro'))
    print(f"Edad calculada2: {edad}")
    if edad is None:
        return {'estado': 'error', 'mensaje': 'fecha_nac_invalida', 'campo': 'fecha_nac_miembro'}


    if edad >= 18:
        campos_obligatorios = [
            'dni_miembro', 'apellido_miembro', 'nombre_miembro',
            'sexo_miembro', 'fecha_nac_miembro', 'nacionalidad_miembro',
            'religion_miembro', 'estado_civil_miembro',
            'caract_miembro', 'telefono_miembro',
            'fecha_afil_miembro', 'funcion_inicial'
        ]
    else:
        campos_obligatorios = [
            'dni_miembro', 'apellido_miembro', 'nombre_miembro',
            'sexo_miembro', 'fecha_nac_miembro', 'nacionalidad_miembro',
            'religion_miembro', 'estado_civil_miembro',
            'caract_miembro', 'telefono_miembro',
            'fecha_afil_miembro', 'funcion_inicial', 'emergencia_miembro'
        ]


    for campo in campos_obligatorios:
        if not datos_form.get(campo):
            return {'estado': 'error', 'mensaje': f'{campo}_vacio', 'campo': 'campo'}

    # ░▒▓ Validación de nombre y apellido ▓▒░
    if len(datos_form['nombre_miembro']) > 50:
        return {'estado': 'error', 'mensaje': 'nombre_largo', 'campo': 'nombre_miembro'}
    if len(datos_form['apellido_miembro']) > 50:
        return {'estado': 'error', 'mensaje': 'apellido_largo', 'campo': 'apellido_miembro'}

    # ░▒▓ Validación de DNI ▓▒░
    dni = datos_form['dni_miembro']
    if not re.fullmatch(r'\d{7,8}', dni):
        return {'estado': 'error', 'mensaje': 'dni_formato_invalido', 'campo': 'dni_miembro'}

    # ░▒▓ Validación de fecha de nacimiento ▓▒░
    try:
        fecha_nac = datetime.strptime(datos_form['fecha_nac_miembro'], '%Y-%m-%d')
        hoy = datetime.today()
        edad = hoy.year - fecha_nac.year - ((hoy.month, hoy.day) < (fecha_nac.month, fecha_nac.day))
        if edad < 6:
            return {'estado': 'error', 'mensaje': 'edad_minima', 'campo': 'fecha_nac_miembro'}
    except:
        return {'estado': 'error', 'mensaje': 'fecha_nac_invalida', 'campo': 'fecha_nac_miembro'}

    # ░▒▓ Validación de teléfono ▓▒░
    caract = datos_form['caract_miembro']
    tel = datos_form['telefono_miembro']
    if not re.fullmatch(r'[1-9][0-9]{1,3}', caract):
        return {'estado': 'error', 'mensaje': 'codigo_area_invalido', 'campo': 'caract_miembro'}
    if not re.fullmatch(r'\d{6,8}', tel):
        return {'estado': 'error', 'mensaje': 'telefono_invalido', 'campo': 'telefono_miembro'}

    # ░▒▓ Validación de email ▓▒░
    mail = datos_form.get('mail_miembro')
    if mail and not re.fullmatch(r'^[^@]+@[^@]+\.[^@]+$', mail):
        return {'estado': 'error', 'mensaje': 'mail_invalido', 'campo': 'mail_miembro'}

    # ░▒▓ Validación nacionalidad ▓▒░
    if datos_form['nacionalidad_miembro'] == 'otro':
        nacion_otro = datos_form.get('nacionalidad_otro', '').strip()
        if not nacion_otro or len(nacion_otro) > 50:
            return {'estado': 'error', 'mensaje': 'nacionalidad_otro_invalido', 'campo': 'nacionalidad_otro'}

    # ░▒▓ Validación dirección (opcional, pero limitada) ▓▒░
    direccion = datos_form.get('direccion_miembro')
    if direccion and len(direccion) > 100:
        return {'estado': 'error', 'mensaje': 'direccion_larga', 'campo': 'direccion_miembro'}

    # ░▒▓ Validación contacto de emergencia ▓▒░
    emergencia = datos_form.get('emergencia_miembro')
    if emergencia and len(emergencia) > 100:
        return {'estado': 'error', 'mensaje': 'emergencia_larga', 'campo': 'emergencia_miembro'}

    # ░▒▓ Validación fecha de afiliación ▓▒░
    try:
        datetime.strptime(datos_form['fecha_afil_miembro'], '%Y-%m-%d')
    except:
        return {'estado': 'error', 'mensaje': 'fecha_afil_invalida', 'campo': 'fecha_afil_miembro'}

    return {'estado': 'ok'}
