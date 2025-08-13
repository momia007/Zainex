"""
░▒▓ Archivo: rutas_contabilidad.py ▓▒░

Este módulo contiene las rutas asociadas al Menú de Contabilidad del sistema,
especialmente aquellas vinculadas a funciones contables como libro caja,
resúmenes financieros, e historial económico. Se asocia al blueprint `admin_bp`.
"""

import cloudinary
import mimetypes
from app.utils.validar_archivo import validar_archivo  # ← Importar el módulo
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
import pymysql
from app.routes.admin import admin_bp  # ← ajustá esto según dónde definas el blueprint
from app.config import conectar_db

@admin_bp.route('/libro_caja')
@login_required
def libro_caja():
    tipo_filtro = request.args.get('tipo')
    rubro_filtro = request.args.get('rubro')
    desde = request.args.get('desde')
    hasta = request.args.get('hasta')

    conn = conectar_db()
    transacciones = []
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
                SELECT m.*, u.nombre_usuario AS creado_por
                FROM movimientos m
                LEFT JOIN usuarios u ON m.creado_por_mov = u.id_usuarios
                WHERE 1=1
            """
            valores = []

            if tipo_filtro:
                query += " AND tipo_mov = %s"
                valores.append(tipo_filtro)

            if rubro_filtro:
                query += " AND rubro_mov = %s"
                valores.append(rubro_filtro)

            if desde and hasta:
                query += " AND fecha_mov BETWEEN %s AND %s"
                valores.extend([desde, hasta])

            query += " ORDER BY fecha_mov ASC, id_mov ASC"
            cursor.execute(query, valores)
            transacciones = cursor.fetchall()

            # Separar saldo inicial antes de calcular
            saldo_inicial = None
            otros_movimientos = []

            for mov in transacciones:
                if mov['detalle_mov'].lower().startswith('saldo inicial'):
                    saldo_inicial = mov
                else:
                    otros_movimientos.append(mov)

            # Ordenar cronológicamente los demás movimientos
            otros_movimientos.sort(key=lambda x: (x['fecha_mov'], x['id_mov']))

            # Usar saldo inicial como punto de partida
            saldo = saldo_inicial['importe_mov'] if saldo_inicial else 0

            # Calcular saldo acumulado
            for mov in otros_movimientos:
                if mov['tipo_mov'] == 'Ingreso':
                    saldo += mov['importe_mov']
                elif mov['tipo_mov'] == 'Egreso':
                    saldo -= mov['importe_mov']
                mov['saldo_actual'] = saldo

            # Agregar saldo inicial al final con su propio saldo
            if saldo_inicial:
                saldo_inicial['saldo_actual'] = saldo_inicial['importe_mov']
                otros_movimientos.append(saldo_inicial)

            # Invertir para mostrar del más reciente al más antiguo
            transacciones = list(reversed(otros_movimientos))

    finally:
        conn.close()

    # Reordenar para que el saldo inicial quede al final visualmente
    transacciones.sort(key=lambda x: x['detalle_mov'].lower().startswith('saldo inicial'))

    return render_template('libro_caja.html', transacciones=transacciones)



@admin_bp.route('/nvo_movimiento', methods=['GET', 'POST'])
@login_required
def nvo_movimiento():
    if request.method == 'POST':
        datos = request.form
        archivo = request.files.get('archivo_comprob')
        url_comprob = None

        es_valido, _ = validar_archivo(archivo)

        if es_valido:
            try:
                # Detectar el tipo MIME del archivo
                tipo_mime, _ = mimetypes.guess_type(archivo.filename)
                es_pdf = tipo_mime == 'application/pdf'

                # Configurar el tipo de recurso según el tipo de archivo
                opciones_upload = {
                    'folder': 'comprobantes_zainex'
                }

                if es_pdf:
                    opciones_upload['resource_type'] = 'raw'

                resultado = cloudinary.uploader.upload(archivo, **opciones_upload)
                url_comprob = resultado.get('secure_url')
                print("Archivo subido a Cloudinary:", url_comprob)

            except Exception as e:
                print("Error al subir a Cloudinary:", e)
                url_comprob = None
        else:
            print("Archivo no válido o vacío")


        conn = conectar_db()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO movimientos (
                        tipo_mov, fecha_mov, detalle_mov, rubro_mov,
                        comprobante_mov, url_comprob_mov, importe_mov,
                        creado_por_mov, observaciones_mov
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    datos.get('tipo_mov'),
                    datos.get('fecha_mov'),
                    datos.get('detalle_mov'),
                    datos.get('rubro_mov'),
                    datos.get('comprobante_mov'),
                    url_comprob,
                    datos.get('importe_mov'),
                    current_user.id,
                    datos.get('observaciones_mov')
                ))
                conn.commit()
                flash('Movimiento registrado exitosamente', 'success')
        finally:
            conn.close()

        return redirect(url_for('admin.libro_caja'))

    return render_template('nvo_movimiento.html')