# ░▒▓ utils/current_user.py ▓▒░
from app.config import conectar_db
from flask_login import current_user
import pymysql

def get_contexto_usuario_actual():
    if current_user.rol_usuario not in ['admin', 'colaborador']:
        return None

    conn = conectar_db()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("""
                SELECT
                    u.id_usuarios,
                    u.nombre_usuario,
                    u.apellido_usuario,
                    u.dni_usuario,
                    u.rol_usuario,
                    g.id_grupo,
                    g.num_grupo,
                    g.nombre_grupo
                FROM usuarios u
                INNER JOIN grupos g ON u.id_grupo = g.id_grupo
                WHERE u.id_usuarios = %s
            """, (current_user.id,))
            return cursor.fetchone()
    finally:
        conn.close()

