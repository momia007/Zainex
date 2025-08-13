import pymysql
import os
from dotenv import load_dotenv
import cloudinary
import cloudinary.uploader

load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')
DB_PORT = int(os.getenv('DB_PORT'))  # ¡Ojo! Convierte el puerto a int

CLOUDINARY_CLOUD_NAME = 'dqgvyrstu'
CLOUDINARY_API_KEY = '387335684694429'
CLOUDINARY_API_SECRET = 'vp-r09SOHBEUSbEnTIVUJ54rGts'

def conectar_db():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=DB_PORT,
        cursorclass=pymysql.cursors.DictCursor
    )
    


cloudinary.config(
    cloud_name = CLOUDINARY_CLOUD_NAME,
    api_key = CLOUDINARY_API_KEY,
    api_secret = CLOUDINARY_API_SECRET,
    secure=True
)
