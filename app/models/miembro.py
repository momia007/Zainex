from app import db

class Miembro(db.Model):
    __tablename__ = 'miembros'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(120), unique=True)
    fecha_ingreso = db.Column(db.Date)
    id_grupo = db.Column(db.Integer, db.ForeignKey('grupos.id_grupo'), nullable=False)
    
    grupo = db.relationship('Grupo', back_populates='miembros')
    funciones_actuales = db.relationship('FuncionMiembro', back_populates='miembro')




    def __repr__(self):
        return f'<Miembro {self.nombre}>'
