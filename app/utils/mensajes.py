# ░▒▓ Conversor de códigos de mensaje a texto legible ▓▒░

def mensaje_legible(codigo):
    mensajes = {
        'nombre_vacio': '⚠️ El campo nombres no puede estar en blanco.',
        'nombre_largo': '⚠️ El/los nombres son demasiado largos.',
        'apellido_vacio': '⚠️ El campo apellido no puede estar en blanco.',
        'apellido_largo': '⚠️ El apellido es demasiado largo.',
        'password_invalido': '⚠️ La contraseña debe tener 6 o más caracteres.',
        'password_no_coincide': '⚠️ Las contraseñas deben ser iguales.',
        'rol_invalido': '⚠️ No tiene permisos para esta acción.',
        'rol_vacio': '⚠️ El campo rol no puede estar vacío.',
        'usuario_duplicado': '⚠️ Ya existe un usuario con ese DNI.',
        'dni_duplicado': '⚠️ Ya existe un miembro con ese DNI.',
        'fecha_invalida': '⚠️ La fecha de nacimiento no es válida.',
        'telefono_invalido': '⚠️ El número de teléfono es incorrecto.',
        'ok': '✅ Operación exitosa.',
    }
    return mensajes.get(codigo, '⚠️ Error desconocido. Verificá los datos.')
