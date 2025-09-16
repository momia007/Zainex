# ░▒▓ models/usuario.py ▓▒░
from flask_login import UserMixin
from app.extensions import db
import bcrypt

class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuarios'

    id_usuarios = db.Column(db.Integer, primary_key=True)
    dni_usuario = db.Column(db.String(20), unique=True, nullable=False)
    nombre_usuario = db.Column(db.String(100), nullable=False)
    apellido_usuario = db.Column(db.String(100), nullable=False)
    pass_usuario_hash = db.Column(db.String(255), nullable=False)
    rol_usuario = db.Column(db.String(20), nullable=False)
    super_admin = db.Column(db.Boolean, default=False)
    id_grupo = db.Column(db.Integer, db.ForeignKey('grupos.id_grupo'), nullable=False)
    creado_en_usuario = db.Column(db.DateTime)
    estado_usuario = db.Column(db.Boolean, default=True)


    grupo = db.relationship('Grupo', back_populates='usuarios')

    def get_id(self):
        return str(self.id_usuarios)

    @staticmethod
    def cargar_por_id(user_id):
        return Usuario.query.filter_by(id_usuarios=user_id).first()

    def __repr__(self):
        return f"<Usuario {self.dni_usuario} - {self.nombre_usuario} {self.apellido_usuario}>"


    def verificar_contrasena(self, contrasena_plana):
        return bcrypt.checkpw(contrasena_plana.encode('utf-8'), self.pass_usuario_hash.encode('utf-8'))
