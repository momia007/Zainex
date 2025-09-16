# ░▒▓ models/grupo.py ▓▒░
from app.extensions import db

class Grupo(db.Model):
    __tablename__ = 'grupos'

    id_grupo = db.Column(db.Integer, primary_key=True)
    nombre_grupo = db.Column(db.String(100), nullable=False)
    num_grupo = db.Column(db.String(20), unique=True, nullable=False)
    distrito_grupo = db.Column(db.String(100))
    zona_grupo = db.Column(db.String(100))
    creado_en_grupo = db.Column(db.DateTime)

    usuarios = db.relationship('Usuario', back_populates='grupo', lazy=True)
    miembros = db.relationship('Miembro', back_populates='grupo', lazy=True)

    def __repr__(self):
        return f"<Grupo {self.num_grupo} - {self.nombre_grupo}>"
