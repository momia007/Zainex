import os
from dotenv import load_dotenv
import cloudinary

# Cargar variables de entorno
env_file = ".env.production" if os.getenv("FLASK_ENV") == "production" else ".env"


# Carga las variables definidas en el archivo .env
load_dotenv(env_file)

# Configuración de Cloudinary
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

def get_database_uri():
    """
    Devuelve la URI de conexión a la base de datos según el entorno actual.

    ENVIRONMENT puede ser:
    - "local": usa los parámetros individuales (host, user, password, etc.)
    - "production": usa la URL completa de Neon definida en NEON_DB_URL

    Esto permite cambiar de entorno fácilmente modificando solo ENVIRONMENT en el .env
    """
    environment = os.getenv("ENVIRONMENT", "local").lower()

    if environment == "production":
        # Producción: conexión a Neon (ya incluye todos los parámetros)
        return os.getenv("NEON_DB_URL")
    else:
        # Desarrollo local: construye la URI con los parámetros individuales
        db_engine = os.getenv("DB_ENGINE", "postgresql")
        db_user = os.getenv("DB_USER", "postgres")
        db_password = os.getenv("DB_PASSWORD", "")
        db_host = os.getenv("DB_HOST", "localhost")
        db_port = os.getenv("DB_PORT", "5432")
        db_name = os.getenv("DB_NAME", "zainex_scout")

        return f"{db_engine}://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

# Clase de configuración principal
class Config:
    SQLALCHEMY_DATABASE_URI = get_database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Cloudinary (por si querés acceder desde app.config)
    CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
    CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
    CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")
