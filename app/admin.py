# app/admin.py  — Blueprint del panel de administrador
from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required
from app.extensions import db
from app.models import Producto, Categoria, Factura, DetalleFactura
from datetime import datetime

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/')
@admin_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('admin/dashboard.html')


# ══ INVENTARIO ══════════════════════════════════════════════

@admin_bp.route('/inventario')
@login_required
def inventario():
    categoria_id  = request.args.get('categoria', type=int)
    estado_filtro = request.args.get('estado', 'todos')
    busqueda      = request.args.get('q', '').strip()

    query = Producto.query.join(Categoria)

    if categoria_id:
        query = query.filter(Producto.categoria_id == categoria_id)
    if estado_filtro == 'disponible':
        query = query.filter(Producto.estado == 'disponible')
    elif estado_filtro == 'agotado':
        query = query.filter(Producto.estado == 'agotado')
    if busqueda:
        query = query.filter(Producto.nombre.ilike(f'%{busqueda}%'))

    productos  = query.order_by(Producto.nombre).all()
    categorias = Categoria.query.order_by(Categoria.nombre).all()
    bajo_stock = Producto.query.filter(
        Producto.stock_actual <= Producto.stock_minimo,
        Producto.estado == 'activo'
    ).count()

    return render_template('admin/inventario.html',
        productos=productos,
        categorias=categorias,
        bajo_stock=bajo_stock,
        categoria_sel=categoria_id,
        estado_sel=estado_filtro,
        busqueda=busqueda
    )


@admin_bp.route('/inventario/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_producto():
    categorias = Categoria.query.order_by(Categoria.nombre).all()
    if request.method == 'POST':
        nombre       = request.form.get('nombre', '').strip()
        categoria_id = request.form.get('categoria_id', type=int)
        descripcion  = request.form.get('descripcion', '').strip()
        precio_venta = request.form.get('precio_venta', type=float)
        stock_actual = request.form.get('stock_actual', type=int)
        stock_minimo = request.form.get('stock_minimo', type=int)
        estado       = request.form.get('estado', 'activo')

        if not nombre or not categoria_id or precio_venta is None:
            flash('Nombre, categoría y precio son obligatorios.', 'error')
            return render_template('admin/inventario_form.html', categorias=categorias, producto=None)

        producto = Producto(
            nombre=nombre, categoria_id=categoria_id,
            descripcion=descripcion, precio_venta=precio_venta,
            stock_actual=stock_actual or 0,
            stock_minimo=stock_minimo or 5,
            estado=estado
        )
        db.session.add(producto)
        db.session.commit()
        flash(f'Producto "{nombre}" creado correctamente.', 'success')
        return redirect(url_for('admin.inventario'))

    return render_template('admin/inventario_form.html', categorias=categorias, producto=None)


@admin_bp.route('/inventario/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_producto(id):
    producto   = Producto.query.get_or_404(id)
    categorias = Categoria.query.order_by(Categoria.nombre).all()

    if request.method == 'POST':
        producto.nombre       = request.form.get('nombre', '').strip()
        producto.categoria_id = request.form.get('categoria_id', type=int)
        producto.descripcion  = request.form.get('descripcion', '').strip()
        producto.precio_venta = request.form.get('precio_venta', type=float)
        producto.stock_actual = request.form.get('stock_actual', type=int)
        producto.stock_minimo = request.form.get('stock_minimo', type=int)
        producto.estado       = request.form.get('estado', 'activo').lower()

        if not producto.nombre or not producto.categoria_id or producto.precio_venta is None:
            return jsonify({'ok': False, 'mensaje': 'Nombre, categoría y precio son obligatorios.'})

        db.session.commit()
        return jsonify({'ok': True, 'mensaje': f'Producto "{producto.nombre}" actualizado.'})

    return jsonify({
        'id':           producto.id,
        'nombre':       producto.nombre,
        'categoria_id': producto.categoria_id,
        'descripcion':  producto.descripcion or '',
        'precio_venta': float(producto.precio_venta),
        'stock_actual': producto.stock_actual,
        'stock_minimo': producto.stock_minimo,
        'estado':       producto.estado,
    })


@admin_bp.route('/inventario/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_producto(id):
    producto = Producto.query.get_or_404(id)
    nombre   = producto.nombre
    db.session.delete(producto)
    db.session.commit()
    return jsonify({'ok': True, 'mensaje': f'Producto "{nombre}" eliminado.'})


# ══ RESTO DE RUTAS ══════════════════════════════════════════

@admin_bp.route('/productos')
@login_required
def productos():
    busqueda    = request.args.get('q', '').strip()
    cat_id      = request.args.get('categoria', type=int)
    estado_sel  = request.args.get('estado', 'todos')
    solo_dest   = request.args.get('destacados', '0') == '1'

    query = Producto.query.join(Categoria)
    if busqueda:
        query = query.filter(Producto.nombre.ilike(f'%{busqueda}%'))
    if cat_id:
        query = query.filter(Producto.categoria_id == cat_id)
    if estado_sel == 'disponible':
        query = query.filter(Producto.estado == 'disponible')
    elif estado_sel == 'agotado':
        query = query.filter(Producto.estado == 'agotado')
    if solo_dest:
        query = query.filter(Producto.destacado == True)

    prods      = query.order_by(Producto.destacado.desc(), Producto.nombre).all()
    categorias = Categoria.query.order_by(Categoria.nombre).all()

    # Stats
    total       = Producto.query.count()
    disponibles = Producto.query.filter_by(estado='disponible').count()
    agotados    = Producto.query.filter_by(estado='agotado').count()
    destacados  = Producto.query.filter_by(destacado=True).count()

    return render_template('admin/productos.html',
        productos=prods,
        categorias=categorias,
        busqueda=busqueda,
        categoria_sel=cat_id,
        estado_sel=estado_sel,
        solo_dest=solo_dest,
        stats={'total': total, 'disponibles': disponibles,
               'agotados': agotados, 'destacados': destacados}
    )


@admin_bp.route('/productos/crear', methods=['POST'])
@login_required
def productos_crear():
    nombre       = request.form.get('nombre', '').strip()
    categoria_id = request.form.get('categoria_id', type=int)
    descripcion  = request.form.get('descripcion', '').strip()
    precio_venta = request.form.get('precio_venta', type=float)
    stock_actual = request.form.get('stock_actual', type=int) or 0
    stock_minimo = request.form.get('stock_minimo', type=int) or 5
    estado       = request.form.get('estado', 'disponible')
    imagen_url   = request.form.get('imagen_url', '').strip() or None

    if not nombre or not categoria_id or precio_venta is None:
        return jsonify({'ok': False, 'mensaje': 'Nombre, categoría y precio son obligatorios.'})

    p = Producto(
        nombre=nombre, categoria_id=categoria_id,
        descripcion=descripcion, precio_venta=precio_venta,
        stock_actual=stock_actual, stock_minimo=stock_minimo,
        estado=estado, imagen_url=imagen_url
    )
    db.session.add(p)
    db.session.commit()
    return jsonify({
        'ok': True,
        'mensaje': f'Producto "{nombre}" creado correctamente.',
        'producto': {
            'id': p.id,
            'nombre': p.nombre,
            'categoria': p.categoria.nombre,
            'categoria_id': p.categoria_id,
            'precio_venta': float(p.precio_venta),
            'stock_actual': p.stock_actual,
            'stock_minimo': p.stock_minimo,
            'estado': p.estado,
            'destacado': p.destacado,
            'imagen_url': p.imagen_url or '',
            'descripcion': p.descripcion or ''
        }
    })


@admin_bp.route('/productos/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def productos_editar(id):
    producto   = Producto.query.get_or_404(id)
    if request.method == 'POST':
        producto.nombre       = request.form.get('nombre', '').strip()
        producto.categoria_id = request.form.get('categoria_id', type=int)
        producto.descripcion  = request.form.get('descripcion', '').strip()
        producto.precio_venta = request.form.get('precio_venta', type=float)
        producto.stock_actual = request.form.get('stock_actual', type=int)
        producto.stock_minimo = request.form.get('stock_minimo', type=int)
        producto.estado       = request.form.get('estado', 'disponible')
        producto.imagen_url   = request.form.get('imagen_url', '').strip() or None

        if not producto.nombre or not producto.categoria_id or producto.precio_venta is None:
            return jsonify({'ok': False, 'mensaje': 'Nombre, categoría y precio son obligatorios.'})

        db.session.commit()
        return jsonify({
            'ok': True,
            'mensaje': f'Producto "{producto.nombre}" actualizado.',
            'producto': {
                'id': producto.id,
                'nombre': producto.nombre,
                'categoria': producto.categoria.nombre,
                'categoria_id': producto.categoria_id,
                'precio_venta': float(producto.precio_venta),
                'stock_actual': producto.stock_actual,
                'stock_minimo': producto.stock_minimo,
                'estado': producto.estado,
                'destacado': producto.destacado,
                'imagen_url': producto.imagen_url or '',
                'descripcion': producto.descripcion or ''
            }
        })

    return jsonify({
        'id':           producto.id,
        'nombre':       producto.nombre,
        'categoria_id': producto.categoria_id,
        'descripcion':  producto.descripcion or '',
        'precio_venta': float(producto.precio_venta),
        'stock_actual': producto.stock_actual,
        'stock_minimo': producto.stock_minimo,
        'estado':       producto.estado,
        'imagen_url':   producto.imagen_url or '',
        'destacado':    producto.destacado,
    })


@admin_bp.route('/productos/eliminar/<int:id>', methods=['POST'])
@login_required
def productos_eliminar(id):
    producto = Producto.query.get_or_404(id)
    nombre   = producto.nombre
    db.session.delete(producto)
    db.session.commit()
    return jsonify({'ok': True, 'mensaje': f'Producto "{nombre}" eliminado.'})


@admin_bp.route('/productos/<int:id>/destacar', methods=['POST'])
@login_required
def productos_destacar(id):
    producto = Producto.query.get_or_404(id)
    producto.destacado = not producto.destacado
    db.session.commit()
    estado = 'destacado' if producto.destacado else 'normal'
    return jsonify({'ok': True, 'destacado': producto.destacado,
                    'mensaje': f'"{producto.nombre}" marcado como {estado}.'})


# ══ CATEGORÍAS ════════════════════════════════════════════════

@admin_bp.route('/categorias', methods=['GET'])
@login_required
def categorias_listar():
    cats = Categoria.query.order_by(Categoria.nombre).all()
    return jsonify([{
        'id': c.id,
        'nombre': c.nombre,
        'total': len(c.productos)
    } for c in cats])


@admin_bp.route('/categorias/crear', methods=['POST'])
@login_required
def categorias_crear():
    nombre = request.form.get('nombre', '').strip()
    if not nombre:
        return jsonify({'ok': False, 'mensaje': 'El nombre es obligatorio.'})
    if Categoria.query.filter_by(nombre=nombre).first():
        return jsonify({'ok': False, 'mensaje': f'La categoría "{nombre}" ya existe.'})
    cat = Categoria(nombre=nombre)
    db.session.add(cat)
    db.session.commit()
    return jsonify({'ok': True, 'mensaje': f'Categoría "{nombre}" creada.',
                    'categoria': {'id': cat.id, 'nombre': cat.nombre, 'total': 0}})


@admin_bp.route('/categorias/eliminar/<int:id>', methods=['POST'])
@login_required
def categorias_eliminar(id):
    cat = Categoria.query.get_or_404(id)
    if cat.productos:
        return jsonify({'ok': False,
                        'mensaje': f'No se puede eliminar: tiene {len(cat.productos)} producto(s) asignado(s).'})
    nombre = cat.nombre
    db.session.delete(cat)
    db.session.commit()
    return jsonify({'ok': True, 'mensaje': f'Categoría "{nombre}" eliminada.'})


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


# ══ FACTURACIÓN ═════════════════════════════════════════════

@admin_bp.route('/facturas')
@login_required
def facturas():
    estado_filtro = request.args.get('estado', 'todas')
    busqueda      = request.args.get('q', '').strip()

    query = Factura.query

    if estado_filtro != 'todas':
        query = query.filter(Factura.estado == estado_filtro)
    if busqueda:
        query = query.filter(Factura.numero.ilike(f'%{busqueda}%'))

    datos = query.order_by(Factura.created_at.desc()).all()

    total_mes = db.session.query(db.func.sum(Factura.total)).filter(Factura.estado == 'pagada').scalar() or 0
    facturas_pend = Factura.query.filter_by(estado='pendiente').count()

    return render_template('admin/facturas.html',
        facturas=datos,
        estado_sel=estado_filtro,
        busqueda=busqueda,
        total_mes=total_mes,
        facturas_pendientes=facturas_pend
    )


@admin_bp.route('/facturas/nueva')
@login_required
def nueva_factura():
    # Generar un número provisional, p.ej. FAC-0000X
    ultimo = Factura.query.order_by(Factura.id.desc()).first()
    siguiente_id = (ultimo.id + 1) if ultimo else 1
    numero_prov = f"FAC-{str(siguiente_id).zfill(5)}"
    
    return render_template('admin/factura_nueva.html', numero_sugerido=numero_prov)


@admin_bp.route('/facturas/productos-json')
@login_required
def productos_json():
    # Retorna JSON para autocompletar, ignorando los agotados
    productos = Producto.query.filter(Producto.estado == 'disponible').order_by(Producto.nombre).all()
    lista = [{
        'id': p.id,
        'nombre': p.nombre,
        'precio': float(p.precio_venta),
        'stock': p.stock_actual
    } for p in productos]
    return jsonify(lista)


@admin_bp.route('/facturas/crear', methods=['POST'])
@login_required
def crear_factura():
    data = request.json
    if not data:
        return jsonify({'ok': False, 'mensaje': 'No se recibieron datos'})

    try:
        nueva_factura = Factura(
            numero=data.get('numero', f"FAC-{datetime.now().strftime('%m%d%H%M%S')}"),
            metodo_pago=data.get('metodo_pago', 'efectivo'),
            estado=data.get('estado', 'pagada'),
            notas=data.get('notas', ''),
            total=data.get('total', 0)
        )
        db.session.add(nueva_factura)
        db.session.flush() # Para obtener el ID

        detalles = data.get('detalles', [])
        for d in detalles:
            prod_id = d['producto_id']
            cant = d['cantidad']
            
            # Crear detalle
            nuevo_det = DetalleFactura(
                factura_id=nueva_factura.id,
                producto_id=prod_id,
                cantidad=cant,
                precio_unitario=d['precio_unitario'],
                subtotal=d['subtotal']
            )
            db.session.add(nuevo_det)

            # Descontar stock
            prod = Producto.query.get(prod_id)
            if prod:
                prod.stock_actual -= cant
                if prod.stock_actual <= 0:
                    prod.stock_actual = 0
                    prod.estado = 'agotado'

        db.session.commit()
        return jsonify({'ok': True, 'mensaje': 'Factura creada exitosamente', 'factura_id': nueva_factura.id})

    except Exception as e:
        db.session.rollback()
        return jsonify({'ok': False, 'mensaje': str(e)})


@admin_bp.route('/facturas/<int:id>')
@login_required
def ver_factura(id):
    factura = Factura.query.get_or_404(id)
    return render_template('admin/factura_detalle.html', factura=factura)


@admin_bp.route('/facturas/<int:id>/imprimir')
@login_required
def imprimir_factura(id):
    factura = Factura.query.get_or_404(id)
    return render_template('admin/factura_imprimir.html', factura=factura)


@admin_bp.route('/facturas/<int:id>/eliminar', methods=['POST'])
@login_required
def eliminar_factura(id):
    factura = Factura.query.get_or_404(id)
    numero = factura.numero
    
    # Restaurar stock
    for det in factura.detalles:
        prod = Producto.query.get(det.producto_id)
        if prod:
            prod.stock_actual += det.cantidad
            if prod.stock_actual > 0 and prod.estado == 'agotado':
                prod.estado = 'disponible'
                
    db.session.delete(factura)
    db.session.commit()
    flash(f'Factura {numero} eliminada y stock restaurado.', 'success')
    return redirect(url_for('admin.facturas'))

