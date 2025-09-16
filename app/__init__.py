
from flask import Flask
from app.config import Config
from flask_login import LoginManager
from app.utils.validar_archivo import validar_archivo
from app.extensions import db  # ← Importás desde extensions
from app.routes.auth import auth_bp
from app.routes.admin import admin_bp
from app.routes.rutas_contabilidad import contabilidad_bp
from app.models.usuario import Usuario  # O el nombre de tu clase/modelo
from app.routes.rutas_miembros import miembros_bp # Importa el blueprint de miembros
from app.routes import rutas_home # Importa las rutas del home
from app.routes import rutas_contabilidad # Importa las rutas de contabilidad


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.cargar_por_id(user_id)  # Reemplazalo con tu método real

    # Configuraciones (pueden ir acá o desde config.py)
    app.secret_key = 'clave_secreta_que_luego_pondrás_en_ENV'


    # Registro de blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(contabilidad_bp)
    return app



