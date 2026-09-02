from flask import Blueprint, render_template
from flask_login import login_required

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/')
@admin_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('admin/dashboard.html')


# ── Rutas placeholder (se implementan en próximos módulos) ───
@admin_bp.route('/inventario')
@login_required
def inventario():
    return render_template('admin/inventario.html')


@admin_bp.route('/productos')
@login_required
def productos():
    return render_template('admin/productos.html')


@admin_bp.route('/productos/nuevo')
@login_required
def nuevo_producto():
    return render_template('admin/nuevo_producto.html')


@admin_bp.route('/ventas')
@login_required
def ventas():
    return render_template('admin/ventas.html')


@admin_bp.route('/ventas/nueva')
@login_required
def nueva_venta():
    return render_template('admin/nueva_venta.html')


@admin_bp.route('/empleados')
@login_required
def empleados():
    return render_template('admin/empleados.html')


@admin_bp.route('/empleados/nuevo')
@login_required
def nuevo_empleado():
    return render_template('admin/nuevo_empleado.html')


@admin_bp.route('/facturas-pendientes')
@login_required
def facturas_pendientes():
    return render_template('admin/facturas_pendientes.html')