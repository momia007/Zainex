from app.config import conectar_db


class Rama:
    def __init__(self, id, nombre, porcentaje_libre):
        self.id = id
        self.nombre = nombre
        self.porcentaje_libre = porcentaje_libre

    @staticmethod
    def listar_todas():
        conn = conectar_db()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id, nombre, porcentaje_libre FROM ramas ORDER BY id")
                resultados = cursor.fetchall()
                return [Rama(**r) for r in resultados]
        finally:
            conn.close()

    @staticmethod
    def obtener_por_id(rama_id):
        conn = conectar_db()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT id, nombre, porcentaje_libre
                    FROM ramas
                    WHERE id = %s
                """, (rama_id,))
                resultado = cursor.fetchone()
                return Rama(**resultado) if resultado else None
        finally:
            conn.close()

