from app import create_app
from app.extensions import db
from sqlalchemy import text

app = create_app()
with app.app_context():
    try:
        db.session.execute(text("ALTER TABLE productos ADD COLUMN destacado TINYINT(1) NOT NULL DEFAULT 0 AFTER estado;"))
        print("Columna 'destacado' añadida.")
    except Exception as e:
        print("Nota (destacado):", e)
        
    try:
        db.session.execute(text("ALTER TABLE productos ADD COLUMN imagen_url VARCHAR(255) NULL DEFAULT NULL AFTER destacado;"))
        print("Columna 'imagen_url' añadida.")
    except Exception as e:
        print("Nota (imagen_url):", e)

    db.session.commit()
    print("Migración completada.")
