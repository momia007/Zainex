"""
░▒▓ Archivo: rutas_home.py ▓▒░

Este módulo contiene las rutas asociadas al menú principal del sistema.
Se asocia al blueprint `admin_bp`.
"""

from flask import render_template
from flask_login import login_required
from app.routes.admin import admin_bp  # ← ajustá esto según dónde definas el blueprint

@admin_bp.route('/contabilidad')
@login_required
def contabilidad():
    return render_template('contabilidad.html')
