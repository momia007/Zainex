from app.config import conectar_db

class Movimiento:
    def __init__(self, fecha_mov, tipo_mov, rubro_mov, importe_mov, detalle_mov, rama_id):
        self.fecha_mov = fecha_mov
        self.tipo_mov = tipo_mov
        self.rubro_mov = rubro_mov
        self.importe_mov = importe_mov
        self.detalle_mov = detalle_mov
        self.rama_id = rama_id

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


    @staticmethod
    def obtener_por_rama(rama_id):
        conn = conectar_db()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT fecha_mov, tipo_mov, rubro_mov, importe_mov, detalle_mov, rama_id
                    FROM movimientos
                    WHERE rama_id = %s
                    ORDER BY fecha_mov DESC
                """, (rama_id,))
                resultados = cursor.fetchall()
                return [Movimiento(**mov) for mov in resultados]
        finally:
            conn.close()

    @staticmethod
    def obtener_por_rama_y_año(rama_id, año):
        conn = conectar_db()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT fecha_mov, tipo_mov, rubro_mov, importe_mov, detalle_mov, rama_id
                    FROM movimientos
                    WHERE rama_id = %s AND YEAR(fecha_mov) = %s
                    ORDER BY fecha_mov DESC
                """, (rama_id, año))
                resultados = cursor.fetchall()
                return [Movimiento(**mov) for mov in resultados]
        finally:
            conn.close()

    @staticmethod
    def calcular_ingresos_por_cuotas(rama_id, año=None):
        conn = conectar_db()
        try:
            with conn.cursor() as cursor:
                if año:
                    cursor.execute("""
                        SELECT SUM(importe_mov)
                        FROM movimientos
                        WHERE rama_id = %s AND tipo_mov = 'Ingreso' AND rubro_mov = 'CUOTA' AND YEAR(fecha_mov) = %s
                    """, (rama_id, año))
                else:
                    cursor.execute("""
                        SELECT SUM(importe_mov)
                        FROM movimientos
                        WHERE rama_id = %s AND tipo_mov = 'Ingreso' AND rubro_mov = 'CUOTA'
                    """, (rama_id,))
                resultado = cursor.fetchone()
                return resultado.get('SUM(importe_mov)', 0) 
                # return resultado['SUM(importe_mov)'] if resultado['SUM(importe_mov)'] else 0
        finally:
            conn.close()

    @staticmethod
    def calcular_egresos(rama_id, año=None):
        conn = conectar_db()
        try:
            with conn.cursor() as cursor:
                if año:
                    cursor.execute("""
                        SELECT SUM(importe_mov)
                        FROM movimientos
                        WHERE rama_id = %s AND tipo_mov = 'Egreso' AND YEAR(fecha_mov) = %s
                    """, (rama_id, año))
                else:
                    cursor.execute("""
                        SELECT SUM(importe_mov)
                        FROM movimientos
                        WHERE rama_id = %s AND tipo_mov = 'Egreso'
                    """, (rama_id,))
                resultado = cursor.fetchone()
                return resultado.get('SUM(importe_mov)', 0)      
                # return resultado['SUM(importe_mov)'] if resultado['SUM(importe_mov)'] else 0
        finally:
            conn.close()
