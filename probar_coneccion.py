from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

# Cargar variables desde el archivo .env
load_dotenv()

# Verificar que la variable esté definida
database_url = os.getenv("DATABASE_URL")
print("🔍 DATABASE_URL:", database_url)

if not database_url:
    raise ValueError("❌ DATABASE_URL no está definida. Verificá el archivo .env y que se haya cargado correctamente.")

# Crear el motor de conexión
engine = create_engine(database_url)

# Probar la conexión
try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("✅ Conexión exitosa:", result.scalar())
except Exception as e:
    print("❌ Error de conexión:", e)
