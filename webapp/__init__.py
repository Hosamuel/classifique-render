import logging
from flask import Flask

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def create_app():
    logger.info("Iniciando aplicação...")
    app = Flask(__name__)
    
    try:
        from .routes import main
        app.register_blueprint(main)
        logger.info("Blueprint registrado com sucesso")
    except Exception as e:
        logger.error(f"Erro ao registrar blueprint: {e}")
        raise
    
    return app

