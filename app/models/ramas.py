# ░▒▓ models/ramas.py ▓▒░
from app.extensions import db


class Rama(db.Model):
    __tablename__ = 'ramas'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    porcentaje_libre = db.Column(db.Float, nullable=False)

    @staticmethod
    def listar_todas():
        return Rama.query.order_by(Rama.id).all()

    @staticmethod
    def obtener_por_id(rama_id):
        return Rama.query.filter_by(id=rama_id).first()
