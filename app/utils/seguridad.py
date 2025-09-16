# ░▒▓ utils/seguridad.py ▓▒░
from werkzeug.security import generate_password_hash, check_password_hash

def hash_clave(clave_plana):
    """Genera un hash seguro para almacenar la clave"""
    return generate_password_hash(clave_plana)

def verificar_clave(clave_plana, clave_hash):
    """Verifica si la clave ingresada coincide con el hash almacenado"""
    return check_password_hash(clave_hash, clave_plana)
