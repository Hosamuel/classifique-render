import logging
import json
import time
from flask import Blueprint, render_template, request, jsonify
from PIL import Image
from webapp.model.predict import classify_image

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


# Caminho para salvar feedbacks
feedback_data = "feedback.json"

@main.route('/feedback', methods=['POST'])
def receive_feedback():
    """Recebe feedback do usuário e armazena no JSON"""
    data = request.get_json()

    try:
        with open(feedback_data, 'a', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)
            f.write("\n")

        return jsonify({"message": "Feedback enviado com sucesso!"}), 200
    except Exception as e:
        logger.error(f"Erro ao salvar feedback: {str(e)}")
        return jsonify({"error": "Erro ao salvar feedback"}), 500

@main.route('/feedbacks-page', methods=['GET'])
def feedbacks_page():
    """Página HTML para exibir os feedbacks"""
    try:
        with open(feedback_data, 'r', encoding='utf-8') as f:
            feedbacks = f.readlines()

        feedback_list = [json.loads(feedback) for feedback in feedbacks]
        return render_template('feedbacks.html', feedbacks=feedback_list)

    except FileNotFoundError:
        return render_template('feedbacks.html', feedbacks=[])

    except Exception as e:
        logger.error(f"Erro ao carregar feedbacks: {str(e)}")
        return render_template('feedbacks.html', feedbacks=[])

