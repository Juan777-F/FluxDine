from flask import Flask
from flask_login import LoginManager
from .extensions import db, csrf

login_manager = LoginManager()

def create_app():
    app = Flask(
        __name__,
        template_folder='templates',
        static_folder='static',
    )

    app.config.from_object('config.Config')

    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.selector'

    from .modules.auth.models import Usuario

    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    from .modules.auth     import auth_bp
    from .modules.admin    import admin_bp
    from .modules.empleado import empleado_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(empleado_bp)

    return app