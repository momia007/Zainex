
from flask import Flask
from flask_login import LoginManager
from app.utils.validar_archivo import validar_archivo
from app.routes.auth import auth_bp
from app.routes.admin import admin_bp
from app.routes.rutas_contabilidad import contabilidad_bp
from app.models.usuario import Usuario  # O el nombre de tu clase/modelo
from app.routes.rutas_miembros import miembros_bp # Importa el blueprint de miembros
from app.routes import rutas_home # Importa las rutas del home
from app.routes import rutas_contabilidad # Importa las rutas de contabilidad


def create_app():
    app = Flask(__name__) # Crea la instancia de Flask
    app.register_blueprint(miembros_bp) # Registra el blueprint de miembros
    app.register_blueprint(contabilidad_bp) # Registra el blueprint de contabilidad


    login_manager = LoginManager()
    # Redirige a la vista de login si no está autenticado
    login_manager.login_view = 'auth.mostrar_loguin'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.cargar_por_id(user_id)  # Reemplazalo con tu método real

    # Configuraciones (pueden ir acá o desde config.py)
    app.secret_key = 'clave_secreta_que_luego_pondrás_en_ENV'


    # Registro de blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)

    return app
