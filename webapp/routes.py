from flask import Blueprint, render_template, request, jsonify # renderiza arquivos HTML do diretório templates, jsonify para as respostas de erro
from PIL import Image
from webapp.model.predict import classify_image

main = Blueprint('main', __name__)# registrando as rotas 

@main.route('/')# pagina de inicio
def index():
    return render_template('index.html')  # renderiza a página inicial

@main.route('/classify', methods=['POST']) # pagina de resul/classificação
def classify():
    if 'image' not in request.files:
        return jsonify({'error': 'Nenhuma imagem enviada'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'Nenhum arquivo selecionado'}), 400

    try:
        image = Image.open(file.stream)  # abrindo a imagem enviada
        result = classify_image(image)  # usando a função do predict.py

        # dividindo os resultados em partes para renderizar no html
        result_lines = result.strip().split('\n')
        parsed_result = {
            "scientific_name": result_lines[0].split(": ")[1],
            "popular_name": result_lines[1].split(": ")[1],
            "link": result_lines[2].split(": ")[1],
            "probability": result_lines[3].split(": ")[1]
        }
        
        return render_template('result.html', result=parsed_result)

    except Exception as e:# capturando o erro e devolvendo a mesagem de erro 
        return jsonify({'error': str(e)}), 500


# Carregando o modelo salvo no arquivo 'model.pth'
model = torch.load(r"webapp\model\model.pth", map_location=torch.device('cpu'), weights_only=True)
