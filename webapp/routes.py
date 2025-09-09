import logging
import time
import os
import re
from flask import Blueprint, render_template, request, jsonify, url_for, session, redirect
from PIL import Image
from webapp.model.predict import classify_image

main = Blueprint('main', __name__, static_folder='../static')

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

LOW_CONFIDENCE_THRESHOLD = 40.0 # Limite de confiança para mensagem (em %)

# Definir corretamente a pasta de uploads
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
WEBAPP_DIR = os.path.dirname(BASE_DIR)  
STATIC_DIR = os.path.join(BASE_DIR, "static") 
UPLOAD_FOLDER = os.path.join(STATIC_DIR, "uploads") 

# Extensões de arquivo permitidas
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

logger.info(f"BASE_DIR: {BASE_DIR}")
logger.info(f"STATIC_DIR: {STATIC_DIR}")
logger.info(f"UPLOAD_FOLDER: {UPLOAD_FOLDER}")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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

# Tempo de retenção para uploads antigos (24 horas)
UPLOAD_RETENTION_TIME_SECONDS = 24 * 60 * 60

def cleanup_old_uploads():
    """Remove arquivos da pasta de uploads que são mais antigos que o tempo de retenção."""
    now = time.time()
    for filename in os.listdir(UPLOAD_FOLDER):
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.isfile(file_path):
            file_age = now - os.path.getmtime(file_path)
            if file_age > UPLOAD_RETENTION_TIME_SECONDS:
                try:
                    os.remove(file_path)
                    logger.info(f"Arquivo antigo removido: {filename}")
                except Exception as e:
                    logger.error(f"Erro ao remover arquivo antigo {filename}: {e}")

@main.route('/')
def home_page():
    return render_template('home.html')

@main.route('/index')
def index_page():
    session['low_confidence_attempts'] = 0 # Reinicia a contagem ao acessar a tela de upload
    return render_template('index.html')

@main.route('/classify', methods=['POST'])
def classify():
    """Recebe uma imagem, classifica e retorna os resultados."""
    low_confidence_message = None
    try:
        logger.info("Iniciando classificação")
        start_time = time.time()

        # Limpa uploads antigos antes de processar um novo
        cleanup_old_uploads()

        if 'image' not in request.files:
            logger.error("Nenhuma imagem enviada")
            return jsonify({'error': 'Nenhuma imagem enviada'}), 400

        file = request.files['image']
        if file.filename == '':
            logger.error("Nenhum arquivo selecionado")
            return jsonify({'error': 'Nenhum arquivo selecionado'}), 400

        if not allowed_file(file.filename):
            logger.error(f"Tipo de arquivo não permitido: {file.filename}")
            return jsonify({'error': 'Tipo de arquivo não permitido. Por favor, envie uma imagem nos formatos PNG, JPG, JPEG ou GIF.'}), 400

        # Processar e salvar a imagem
        try:
            image = Image.open(file.stream)
        except (Image.UnidentifiedImageError, IOError) as e:
            logger.error(f"Erro ao abrir a imagem: {e}")
            return jsonify({'error': 'Não foi possível abrir a imagem. Certifique-se de que o arquivo é uma imagem válida e não está corrompido.'}), 400
        
        image = image.convert('RGB') # Garante que a imagem tenha 3 canais (RGB)
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
        results, top_probability = classify_image(image) # Pega a probabilidade numérica
        logger.info(f"Classificação concluída em {time.time() - start_time:.2f}s")

        # Lógica de baixa confiança
        if top_probability < LOW_CONFIDENCE_THRESHOLD:
            session['low_confidence_attempts'] = session.get('low_confidence_attempts', 0) + 1
            if session['low_confidence_attempts'] == 1:
                low_confidence_message = "Confiança baixa na classificação. Tente novamente com a mesma planta em ângulos e iluminação diferentes para melhores resultados!"
            else:
                low_confidence_message = "Ainda não foi possível classificar com alta confiança. Talvez esta planta não esteja em nosso banco de dados, mas estamos sempre ampliando a cobertura do DeepFlora!"
        else:
            session['low_confidence_attempts'] = 0 # Reseta a contagem se a confiança for alta

        # Renderizar diretamente o template com os resultados
        return render_template('result.html', 
                             results=results,
                             image_url=image_url,
                             low_confidence_message=low_confidence_message)

    except Exception as e:
        logger.error(f"Erro durante classificação: {str(e)}")
        return jsonify({'error': 'Erro interno. Tente novamente.'}), 500
