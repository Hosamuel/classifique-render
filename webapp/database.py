from flask_sqlalchemy import SQLAlchemy

# Criamos uma instância do SQLAlchemy
db = SQLAlchemy()

# Modelo para armazenar feedbacks
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    correct = db.Column(db.Boolean, nullable=False)
    correct_name = db.Column(db.String(255), nullable=True)

    def __init__(self, correct, correct_name=None):
        self.correct = correct
        self.correct_name = correct_name
