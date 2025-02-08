from webapp.database import db, Feedback
from webapp import create_app

# Criar a aplicação e o banco de dados
app = create_app()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa o banco de dados
db.init_app(app)

with app.app_context():
    db.create_all()
    print("Banco de dados inicializado!")
