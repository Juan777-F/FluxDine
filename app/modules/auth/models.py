# app/modules/auth/models.py
from flask_login import UserMixin
from app.extensions import db

class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'

    id               = db.Column(db.Integer, primary_key=True)
    rol_id           = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    username         = db.Column(db.String(50), unique=True, nullable=False)
    password_hash    = db.Column(db.String(255), nullable=False)
    nombre_completo  = db.Column(db.String(100), nullable=False)
    email            = db.Column(db.String(100), unique=True, nullable=False)
    estado           = db.Column(db.Enum('activo', 'inactivo'), default='activo')

    rol = db.relationship('Rol', backref='usuarios')

    def check_password(self, password):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password_hash, password)


class Rol(db.Model):
    __tablename__ = 'roles'

    id     = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)