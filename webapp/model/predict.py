import torch
import json
import torchvision.transforms as transforms
from torchvision import models
from pathlib import Path

# Caminhos do modelo e JSON
current_dir = Path(__file__).parent
json_path = current_dir / "new_names.json"
model_path = current_dir / "pesos_it_1.pth"

# Verifica se o modelo existe
if not model_path.exists():
    raise FileNotFoundError(f"Arquivo de pesos do modelo não encontrado: {model_path}")

# Carregar classes do JSON
with open(json_path, 'r', encoding='utf-8') as f:
    class_data = json.load(f)

# Organizando classes em ordem alfabética
sorted_class_data = sorted(class_data.items(), key=lambda x: x[1]["nomes_cientificos"][0])
class_names = [data[1]["nomes_cientificos"][0] for data in sorted_class_data]
class_populares = [data[1]["nomes_populares"][0] for data in sorted_class_data]
class_links = [data[1]["link"] for data in sorted_class_data]
num_classes = len(class_names)

# Cache do modelo
_model = None

def load_model():
    """Carrega o modelo ResNet50 com os pesos treinados."""
    model = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V1)
    num_ftrs = model.fc.in_features
    model.fc = torch.nn.Linear(num_ftrs, num_classes)

    # Carregar pesos treinados
    model.load_state_dict(torch.load(str(model_path), map_location=torch.device('cpu')))
    model.eval()
    return model

def get_model():
    """Retorna o modelo carregado, usando cache para eficiência."""
    global _model
    if _model is None:
        _model = load_model()
    return _model

# Transformações para pré-processar a imagem
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# Função para classificar a imagem
def classify_image(image):
    """Recebe uma imagem PIL, faz a predição e retorna o resultado formatado."""
    model = get_model()  # Usa modelo em cache
    image = preprocess(image).unsqueeze(0)  # Adiciona dimensão extra

    with torch.no_grad():  # Desativa cálculo de gradientes
        outputs = model(image)
        probabilities = torch.nn.functional.softmax(outputs, dim=1)[0]  # Probabilidades por classe
        top_prob, top_catid = torch.max(probabilities, 0)  # Classe com maior probabilidade
    
    # Extração das informações
    scientific_name = class_names[top_catid.item()]
    popular_name = class_populares[top_catid.item()]
    link = class_links[top_catid.item()]
    prob = top_prob.item() * 100  # Convertendo para %

    # Formatação do resultado
    result = {
        "scientific_name": scientific_name,
        "popular_name": popular_name,
        "link": link,
        "probability": f"{prob:.2f}%"
    }

    return result
