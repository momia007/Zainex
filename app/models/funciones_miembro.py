from app.models.miembro import Miembro
from app import db

def obtener_miembro_por_id(miembro_id):
    return Miembro.query.get(miembro_id)

def crear_miembro(nombre, correo, fecha_ingreso):
    nuevo = Miembro(nombre=nombre, correo=correo, fecha_ingreso=fecha_ingreso)
    db.session.add(nuevo)
    db.session.commit()
    return nuevo

def eliminar_miembro(miembro_id):
    miembro = Miembro.query.get(miembro_id)
    if miembro:
        db.session.delete(miembro)
        db.session.commit()
        return True
    return False

class FuncionMiembro(db.Model):
    __tablename__ = 'funciones_miembro'

    id_funcion_miembro = db.Column(db.Integer, primary_key=True)
    id_funcion = db.Column(db.Integer, db.ForeignKey('funciones.id_funcion'), nullable=False)
    id_miembro = db.Column(db.Integer, db.ForeignKey('miembros.id'), nullable=False)
    desde_fecha = db.Column(db.Date)
    hasta_fecha = db.Column(db.Date)

    funcion = db.relationship('Funcion', back_populates='asignaciones')
    miembro = db.relationship('Miembro', back_populates='funciones_actuales')