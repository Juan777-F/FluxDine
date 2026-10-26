# app/auth.py  — Blueprint de autenticación
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from app.models import Usuario

auth_bp = Blueprint('auth', __name__)


# ── Selector de rol (pantalla de inicio / raíz) ──────────────
@auth_bp.route('/')
@auth_bp.route('/selector')
def selector():
    return render_template('auth/selector.html')


# ── Login Administrador ──────────────────────────────────────
@auth_bp.route('/login/admin', methods=['GET', 'POST'])
def login_admin():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        usuario = Usuario.query.filter_by(username=username, estado='activo').first()
        if usuario and usuario.check_password(password) and usuario.rol.nombre == 'Administrador':
            login_user(usuario)
            return redirect(url_for('admin.dashboard'))
        flash('Credenciales incorrectas.', 'error')

    return render_template('auth/login_admin.html')


# ── Login Empleado ───────────────────────────────────────────
@auth_bp.route('/login/empleado', methods=['GET', 'POST'])
def login_empleado():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        usuario = Usuario.query.filter_by(username=username, estado='activo').first()
        if usuario and usuario.check_password(password) and usuario.rol.nombre != 'Administrador':
            login_user(usuario)
            return redirect(url_for('empleado.panel'))
        flash('Credenciales incorrectas.', 'error')

    return render_template('auth/login_empleado.html')


# ── Logout ───────────────────────────────────────────────────
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.selector'))
