# ░▒▓ models/funcion.py ▓▒░
from app.extensions import db

class Funcion(db.Model):
    __tablename__ = 'funciones'

    id_funcion = db.Column(db.Integer, primary_key=True)
    nombre_funcion = db.Column(db.String(100), nullable=False)
    tipo_funcion = db.Column(db.String(50))  # Ej: 'rama', 'grupo', 'distrito'

    miembros = db.relationship('FuncionMiembro', back_populates='funcion', lazy=True)
    asignaciones = db.relationship('FuncionMiembro', back_populates='funcion')


    def __repr__(self):
        return f"<Funcion {self.nombre_funcion} ({self.tipo_funcion})>"
