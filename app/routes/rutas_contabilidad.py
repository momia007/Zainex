"""
░▒▓ Archivo: rutas_contabilidad.py ▓▒░

Este módulo contiene las rutas asociadas al Menú de Contabilidad del sistema,
especialmente aquellas vinculadas a funciones contables como libro caja,
resúmenes financieros, e historial económico. Se asocia al blueprint `admin_bp`.
"""

import cloudinary
import cloudinary.uploader
from datetime import datetime
import mimetypes
from app.utils.validar_archivo import validar_archivo  # ← Importar el módulo
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.routes.admin import admin_bp  # ← ajustá esto según dónde definas el blueprint
from flask import Blueprint, render_template, request
from app.models.movimientos import Movimiento
from app.models.ramas import Rama
from sqlalchemy import and_
from app.extensions import db
from app.models.movimientos import Movimiento
from app.models.usuario import Usuario  # si querés mostrar el nombre del creador

@admin_bp.route('/libro_caja')
@login_required
def libro_caja():
    tipo_filtro = request.args.get('tipo')
    rubro_filtro = request.args.get('rubro')
    desde = request.args.get('desde')
    hasta = request.args.get('hasta')

    filtros = []

    if tipo_filtro:
        filtros.append(Movimiento.tipo_mov == tipo_filtro)
    if rubro_filtro:
        filtros.append(Movimiento.rubro_mov == rubro_filtro)
    if desde and hasta:
        filtros.append(Movimiento.fecha_mov.between(desde, hasta))

    movimientos = db.session.query(Movimiento).filter(and_(*filtros)).order_by(
        Movimiento.fecha_mov.asc(), Movimiento.id_mov.asc()
    ).all()

    saldo_inicial = next((m for m in movimientos if m.detalle_mov.lower().startswith('saldo inicial')), None)
    otros_movimientos = [m for m in movimientos if m != saldo_inicial]

    saldo = saldo_inicial.importe_mov if saldo_inicial else 0
    for mov in otros_movimientos:
        if mov.tipo_mov == 'Ingreso':
            saldo += mov.importe_mov
        elif mov.tipo_mov == 'Egreso':
            saldo -= mov.importe_mov
        mov.saldo_actual = saldo

    if saldo_inicial:
        saldo_inicial.saldo_actual = saldo_inicial.importe_mov
        otros_movimientos.append(saldo_inicial)

    transacciones = list(reversed(otros_movimientos))
    transacciones.sort(key=lambda x: x.detalle_mov.lower().startswith('saldo inicial'))

    return render_template('libro_caja.html', transacciones=transacciones)

"""     # Reordenar para que el saldo inicial quede al final visualmente
    transacciones.sort(key=lambda x: x['detalle_mov'].lower().startswith('saldo inicial'))

    return render_template('libro_caja.html', transacciones=transacciones) """



@admin_bp.route('/nvo_movimiento', methods=['GET', 'POST'])
@login_required
def nvo_movimiento():
    if request.method == 'POST':
        datos = request.form
        print("📨 Datos recibidos:", datos)
        archivo = request.files.get('archivo_comprob')
        url_comprob = None

        es_valido, _ = validar_archivo(archivo)

        if es_valido:
            try:
                import os   # Asegurarse de importar os que maneja tipos MIME (nombres de archivos y extensiones)
                tipo_mime, _ = mimetypes.guess_type(archivo.filename)
                es_pdf = tipo_mime == 'application/pdf'
                opciones_upload = {'folder': 'comprobantes_zainex'}
                # Verificamos si es PDF o imagen
                tipo_mime, _ = mimetypes.guess_type(archivo.filename)
                es_pdf = tipo_mime == 'application/pdf'

                opciones_upload = {'folder': 'comprobantes_zainex'}

                nombre_base, ext = os.path.splitext(archivo.filename)

                if es_pdf:
                    # PDF → se sube como raw, se mantiene extensión .pdf
                    opciones_upload['public_id'] = f"comprobantes_zainex/{nombre_base}"
                    opciones_upload['resource_type'] = 'raw'
                else:
                    # Imagen → se sube como image, se mantiene su extensión original
                    opciones_upload['public_id'] = f"comprobantes_zainex/{nombre_base}"
                    opciones_upload['resource_type'] = 'image'

                resultado = cloudinary.uploader.upload(archivo, **opciones_upload)
                url_comprob = resultado.get('secure_url')
                print("✅ URL subida:", url_comprob)
            except Exception as e:
                print("❌ Error al subir a Cloudinary:", e)
        
        rama_id_raw = datos.get('rama_id')
        rama_id = int(rama_id_raw) if rama_id_raw else None
        
        print("📎 Archivo recibido:", archivo.filename if archivo else "No hay archivo")
        print("🌐 URL generada:", url_comprob)
        print("🆔 Rama ID crudo:", rama_id_raw)
        print("🔢 Rama ID convertido:", rama_id)

        nuevo_mov = Movimiento(
            tipo_mov=datos.get('tipo_mov'),
            fecha_mov=datos.get('fecha_mov'),
            detalle_mov=datos.get('detalle_mov'),
            rubro_mov=datos.get('rubro_mov'),
            comprobante_mov=datos.get('comprobante_mov'),
            url_comprob_mov=url_comprob,
            importe_mov=datos.get('importe_mov'),
            creado_por_mov=current_user.id_usuarios,
            creado_en_mov=datetime.now(),
            observaciones_mov=datos.get('observaciones_mov'),
            rama_id=rama_id,
            conciliado_por_mov=None
        )
        
        print("🧾 Movimiento a guardar:", nuevo_mov.__dict__)

        db.session.add(nuevo_mov)
        db.session.commit()
        flash('Movimiento registrado exitosamente', 'success')
        return redirect(url_for('admin.libro_caja'))

    ramas = Rama.listar_todas()
    return render_template('nvo_movimiento.html', ramas=ramas)



contabilidad_bp = Blueprint('contabilidad', __name__, url_prefix='/contabilidad')

@contabilidad_bp.route('/saldos_rama', methods=['GET', 'POST'])
def saldos_rama():
    ramas = Rama.listar_todas()
    movimientos_filtrados = []
    rama_seleccionada = None
    saldo_libre = None
    porcentaje = None
    año_seleccionado = None
    años_disponibles = Movimiento.obtener_años_con_movimientos()

    if request.method == 'POST':
        # 👇 Acá va el bloque que estás preguntando
        rama_id_raw = request.form.get('rama_id')
        año_raw = request.form.get('año')
        print("Datos recibidos:", rama_id_raw, año_raw)

        try:
            rama_id = int(rama_id_raw)
            año_seleccionado = int(año_raw)
        except Exception as e:
            print("Error al convertir rama_id o año:", e)
            return render_template('saldos_rama.html',
                                   ramas=ramas,
                                   movimientos=[],
                                   error="Datos inválidos en el formulario.")

        # 👇 Continúa el flujo normal
        rama_seleccionada = Rama.obtener_por_id(rama_id)
        if not rama_seleccionada:
            print(f"⚠️ No se encontró la rama con ID: {rama_id}")
            return render_template('saldos_rama.html',
                                ramas=ramas,
                                movimientos=[],
                                rama_seleccionada=None,
                                saldo_libre=None,
                                porcentaje=None,
                                año_seleccionado=año_seleccionado,
                                error="La rama seleccionada no existe.")


        movimientos_filtrados = Movimiento.obtener_por_rama_y_año(rama_id, año_seleccionado)
        total_ingresos = Movimiento.calcular_ingresos_por_cuotas(rama_id, año_seleccionado)
        total_gastos = Movimiento.calcular_egresos(rama_id, año_seleccionado)

        total_ingresos = total_ingresos or 0
        total_gastos = total_gastos or 0

        porcentaje = rama_seleccionada.porcentaje_libre or 10
        saldo_libre = round((total_ingresos * porcentaje / 100) - total_gastos, 2)
        print(f"Movimientos encontrados para rama {rama_id} en {año_seleccionado}: {len(movimientos_filtrados)}")

        

    return render_template('saldos_rama.html',
                           ramas=ramas,
                           movimientos=movimientos_filtrados,
                           rama_seleccionada=rama_seleccionada,
                           saldo_libre=saldo_libre,
                           porcentaje=porcentaje,
                           año_seleccionado=año_seleccionado,
                           años=años_disponibles)
