# ░▒▓ models/movimientos.py ▓▒░
from app.extensions import db
from datetime import datetime
from sqlalchemy import extract

class Movimiento(db.Model):
    __tablename__ = 'movimientos'

    id_mov = db.Column(db.Integer, primary_key=True)
    fecha_mov = db.Column(db.DateTime, nullable=False)
    tipo_mov = db.Column(db.String(20), nullable=False)
    rubro_mov = db.Column(db.String(50), nullable=False)
    comprobante_mov = db.Column(db.String(50))
    url_comprob_mov = db.Column(db.String(255))
    creado_en_mov = db.Column(db.DateTime)
    creado_por_mov = db.Column(db.Integer)
    conciliado_por_mov = db.Column(db.Integer)
    observaciones_mov = db.Column(db.Text)
    importe_mov = db.Column(db.Float, nullable=False)
    detalle_mov = db.Column(db.String(255))
    rama_id = db.Column(db.Integer, db.ForeignKey('ramas.id'), nullable=True)

    rama = db.relationship('Rama', backref='movimientos')

    @staticmethod
    def obtener_años_con_movimientos():
        años = db.session.query(extract('year', Movimiento.fecha_mov)).distinct().order_by(extract('year', Movimiento.fecha_mov)).all()
        return [int(a[0]) for a in años]


    @staticmethod
    def obtener_por_rama(rama_id):
        return Movimiento.query.filter_by(rama_id=rama_id).order_by(Movimiento.fecha_mov.desc()).all()

    @staticmethod
    def obtener_por_rama_y_año(rama_id, año):
        return Movimiento.query.filter(
            Movimiento.rama_id == rama_id,
            db.extract('year', Movimiento.fecha_mov) == año
        ).order_by(Movimiento.fecha_mov.desc()).all()

    @staticmethod
    def calcular_ingresos_por_cuotas(rama_id, año=None):
        query = Movimiento.query.filter_by(
            rama_id=rama_id,
            tipo_mov='Ingreso',
            rubro_mov='CUOTA'
        )
        if año:
            query = query.filter(db.extract('year', Movimiento.fecha_mov) == año)
        total = query.with_entities(db.func.sum(Movimiento.importe_mov)).scalar()
        return total or 0

    @staticmethod
    def calcular_egresos(rama_id, año=None):
        query = Movimiento.query.filter_by(
            rama_id=rama_id,
            tipo_mov='Egreso'
        )
        if año:
            query = query.filter(db.extract('year', Movimiento.fecha_mov) == año)
        total = query.with_entities(db.func.sum(Movimiento.importe_mov)).scalar()
        return total or 0
