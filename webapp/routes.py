import logging
from flask import Blueprint, render_template, request, jsonify
from PIL import Image
import time
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
        result = classify_image(image)
        logger.info(f"Classificação concluída em {time.time() - start_time:.2f}s")

        try:
            result_lines = result.strip().split('\n')
            parsed_result = {
                "scientific_name": result_lines[0].split(": ")[1],
                "popular_name": result_lines[1].split(": ")[1],
                "link": result_lines[2].split(": ")[1],
                "probability": result_lines[3].split(": ")[1]
            }
        except IndexError:
            logger.error("Erro ao processar os resultados")
            return jsonify({'error': 'Erro ao processar os resultados da classificação.'}), 500

        logger.info("Retornando resultado")
        return render_template('result.html', result=parsed_result)

    except Exception as e:
        logger.error(f"Erro durante classificação: {str(e)}")
        return jsonify({'error': 'Erro interno. Tente novamente.'}), 500
