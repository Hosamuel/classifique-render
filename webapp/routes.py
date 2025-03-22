import logging
import time
import os
import re
from flask import Blueprint, render_template, request, jsonify, url_for
from PIL import Image
from webapp.model.predict import classify_image

main = Blueprint('main', __name__, static_folder='../static')

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Definir corretamente a pasta de uploads
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
WEBAPP_DIR = os.path.dirname(BASE_DIR)  
STATIC_DIR = os.path.join(BASE_DIR, "static") 
UPLOAD_FOLDER = os.path.join(STATIC_DIR, "uploads") 

logger.info(f"BASE_DIR: {BASE_DIR}")
logger.info(f"STATIC_DIR: {STATIC_DIR}")
logger.info(f"UPLOAD_FOLDER: {UPLOAD_FOLDER}")

if not os.path.exists(UPLOAD_FOLDER):
    logger.warning(f"Diretório de uploads não encontrado em {UPLOAD_FOLDER}. Verifique se a estrutura de pastas está correta.")
    raise RuntimeError(f"Diretório de uploads não encontrado em {UPLOAD_FOLDER}")

# Armazena os últimos resultados de classificação e imagem
last_classification_results = []
last_uploaded_image = None

def sanitize_filename(filename):
    """Remove caracteres especiais e substitui espaços no nome do arquivo."""
    filename = filename.strip().replace(" ", "_")  
    filename = re.sub(r"[^\w\-.]", "", filename) 
    return filename

@main.route('/')
def home():
    return render_template('index.html')

@main.route('/classify', methods=['POST'])
def classify():
    """Recebe uma imagem, classifica e retorna os resultados."""
    try:
        logger.info("Iniciando classificação")
        start_time = time.time()

        if 'image' not in request.files:
            logger.error("Nenhuma imagem enviada")
            return jsonify({'error': 'Nenhuma imagem enviada'}), 400

        file = request.files['image']
        if file.filename == '':
            logger.error("Nenhum arquivo selecionado")
            return jsonify({'error': 'Nenhum arquivo selecionado'}), 400

        # Processar e salvar a imagem
        image = Image.open(file.stream)
        max_size = (800, 800)
        image.thumbnail(max_size, Image.Resampling.LANCZOS)

        # Criar um nome de arquivo
        timestamp = int(time.time())
        sanitized_filename = sanitize_filename(file.filename)
        image_filename = f"{timestamp}_{sanitized_filename}"
        image_path = os.path.join(UPLOAD_FOLDER, image_filename)

        # Salvar a imagem
        image.save(image_path)

        image_url = url_for('static', filename=f'uploads/{image_filename}', _external=False)

        logger.info(f"Imagem salva corretamente: {image_path}")

        logger.info("Iniciando classificação da imagem")
        results = classify_image(image)
        logger.info(f"Classificação concluída em {time.time() - start_time:.2f}s")

        # Renderizar diretamente o template com os resultados
        return render_template('result.html', 
                             results=results,
                             image_url=image_url)

    except Exception as e:
        logger.error(f"Erro durante classificação: {str(e)}")
        return jsonify({'error': 'Erro interno. Tente novamente.'}), 500
