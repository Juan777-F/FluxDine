# app/models.py  — Todos los modelos de la base de datos
from flask_login import UserMixin
from app.extensions import db
from datetime import datetime


# ══ AUTH ════════════════════════════════════════════════════════

class Rol(db.Model):
    __tablename__ = 'roles'

    id     = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)


class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'

    id              = db.Column(db.Integer, primary_key=True)
    rol_id          = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    username        = db.Column(db.String(50), unique=True, nullable=False)
    password_hash   = db.Column(db.String(255), nullable=False)
    nombre_completo = db.Column(db.String(100), nullable=False)
    email           = db.Column(db.String(100), unique=True, nullable=False)
    estado          = db.Column(db.Enum('activo', 'inactivo'), default='activo')

    rol = db.relationship('Rol', backref='usuarios')

    def check_password(self, password):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password_hash, password)


# ══ INVENTARIO ══════════════════════════════════════════════════

class Categoria(db.Model):
    __tablename__ = 'categorias'

    id     = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)

    productos = db.relationship('Producto', backref='categoria', lazy=True)

    def __repr__(self):
        return f'<Categoria {self.nombre}>'


class Producto(db.Model):
    __tablename__ = 'productos'

    id           = db.Column(db.Integer, primary_key=True)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)
    nombre       = db.Column(db.String(100), nullable=False)
    descripcion  = db.Column(db.Text)
    precio_venta = db.Column(db.Numeric(10, 2), nullable=False)
    stock_actual = db.Column(db.Integer, default=0)
    stock_minimo = db.Column(db.Integer, default=5)
    estado       = db.Column(db.Enum('disponible', 'agotado'), default='disponible')
    destacado    = db.Column(db.Boolean, default=False)
    imagen_url   = db.Column(db.String(255), nullable=True)
    created_at   = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at   = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Producto {self.nombre}>'

    @property
    def bajo_stock(self):
        return self.stock_actual <= self.stock_minimo

# ══ FACTURACIÓN ═════════════════════════════════════════════════

class Factura(db.Model):
    __tablename__ = 'facturas'

    id          = db.Column(db.Integer, primary_key=True)
    numero      = db.Column(db.String(20), unique=True, nullable=False)
    fecha       = db.Column(db.DateTime, default=datetime.utcnow)
    metodo_pago = db.Column(db.Enum('efectivo', 'transferencia', 'tarjeta'), nullable=False)
    estado      = db.Column(db.Enum('pagada', 'pendiente', 'anulada'), default='pagada')
    total       = db.Column(db.Numeric(12, 2), nullable=False, default=0.00)
    notas       = db.Column(db.Text, nullable=True)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at  = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    detalles = db.relationship('DetalleFactura', backref='factura', cascade='all, delete-orphan', lazy=True)

    def __repr__(self):
        return f'<Factura {self.numero}>'

class DetalleFactura(db.Model):
    __tablename__ = 'detalle_facturas'

    id              = db.Column(db.Integer, primary_key=True)
    factura_id      = db.Column(db.Integer, db.ForeignKey('facturas.id', ondelete='CASCADE'), nullable=False)
    producto_id     = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    cantidad        = db.Column(db.Integer, nullable=False, default=1)
    precio_unitario = db.Column(db.Numeric(10, 2), nullable=False)
    subtotal        = db.Column(db.Numeric(12, 2), nullable=False)

    producto = db.relationship('Producto')

    def __repr__(self):
        return f'<DetalleFactura Factura:{self.factura_id} Producto:{self.producto_id}>'
