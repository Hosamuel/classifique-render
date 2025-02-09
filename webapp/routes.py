import logging
import time
from flask import Blueprint, render_template, request, jsonify
from PIL import Image
from webapp.model.predict import classify_image
from webapp.database import db, Feedback

main = Blueprint('main', __name__)

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@main.route('/')
def home():
    return render_template('index.html')

@main.route('/classify', methods=['POST'])
def classify():
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

        # Limitar tamanho da imagem
        image = Image.open(file.stream)
        max_size = (800, 800)
        image.thumbnail(max_size, Image.Resampling.LANCZOS)

        logger.info("Iniciando classificação da imagem")
        results = classify_image(image)
        logger.info(f"Classificação concluída em {time.time() - start_time:.2f}s")

        logger.info("Retornando resultado")
        return render_template('result.html', results=results)

    except Exception as e:
        logger.error(f"Erro durante classificação: {str(e)}")
        return jsonify({'error': 'Erro interno. Tente novamente.'}), 500

@main.route('/feedback', methods=['POST'])
def receive_feedback():
    """Recebe feedback do usuário e salva no banco de dados"""
    data = request.get_json()

    try:
        feedback_entry = Feedback(correct=data['correct'], correct_name=data.get('correct_name'))
        db.session.add(feedback_entry)
        db.session.commit()

        return jsonify({"message": "Feedback salvo com sucesso!"}), 200
    except Exception as e:
        logger.error(f"Erro ao salvar feedback: {str(e)}")
        return jsonify({"error": "Erro ao salvar feedback"}), 500