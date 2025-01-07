from flask import Flask

def create_app():# definindo a aplicação e configuração do flask
    webapp = Flask(__name__)# instancia, "name" fará a localização dos templates

    # Configurações do Flask
    webapp.config['SECRET_KEY'] = 'senha_teste'

    # Registro de rotas, que seram conectadas ao routes.py
    from .routes import main
    webapp.register_blueprint(main)# facilita/organiza a conecção das rotas na aplicação 

    return webapp

