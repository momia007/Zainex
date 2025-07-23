from flask_login import UserMixin
from app.config import conectar_db  # Tu función para conectar a la DB

class Usuario(UserMixin):
    def __init__(self, id, dni, nombre, rol, super_admin, id_grupo):
        self.id = id
        self.dni = dni
        self.nombre = nombre
        self.rol_usuario = rol
        self.super_admin = super_admin
        self.id_grupo = id_grupo

    @staticmethod
    def cargar_por_id(user_id):
        conn = conectar_db()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM usuarios WHERE id_usuarios = %s", (user_id,))
                datos = cursor.fetchone()

                if datos:
                    return Usuario(
                        id=datos["id_usuarios"],
                        dni=datos["dni_usuario"],
                        nombre=datos["nombre_usuario"],
                        rol=datos["rol_usuario"],
                        super_admin=datos["super_admin"],
                        id_grupo=datos["id_grupo"]
                    )
                else:
                    return None
        finally:
            conn.close()
