from flask import Blueprint, render_template
from flask_login import login_required

empleado_bp = Blueprint('empleado', __name__, url_prefix='/empleado')

@empleado_bp.route('/')
@empleado_bp.route('/panel')
@login_required
def panel():
    return render_template('empleado/panel.html')

@empleado_bp.route('/productos')
@login_required
def productos():
    return render_template('empleado/productos.html')

@empleado_bp.route('/ventas/nueva')
@login_required
def nueva_venta():
    return render_template('empleado/nueva_venta.html')

@empleado_bp.route('/ventas/mis-ventas')
@login_required
def mis_ventas():
    return render_template('empleado/mis_ventas.html')