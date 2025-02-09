from flask_sqlalchemy import SQLAlchemy

# Inicializa o banco de dados
db = SQLAlchemy()

class Feedback(db.Model):
    """Modelo para armazenar feedback dos usuários"""
    id = db.Column(db.Integer, primary_key=True)
    correct = db.Column(db.Boolean, nullable=False)
    correct_name = db.Column(db.String(255), nullable=True)

def init_db(app):
    """Inicializa o banco de dados com a aplicação Flask"""
    db.init_app(app)
    with app.app_context():
        db.create_all()  # Cria as tabelas


