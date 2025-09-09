import torch
import json
import torchvision.transforms as transforms
from torchvision import models
from pathlib import Path
import gdown  

current_dir = Path(__file__).parent
json_path = current_dir / "new_names.json"
model_path = current_dir / "pesos_it_1.pth"

# Link do Google Drive 
gdrive_url = "https://drive.google.com/uc?id=1lgf7BMMPLz5sHSbOIAwcII6l04x4Ijy6"

# Baixar pesos do Google Drive
if not model_path.exists():
    print("Pesos do modelo não encontrados. Baixando do Google Drive...")
    gdown.download(gdrive_url, str(model_path), quiet=False)
    print(f"Modelo salvo em: {model_path}")

if not model_path.exists():
    raise FileNotFoundError(f"Erro: O arquivo de pesos do modelo não foi encontrado ou não pôde ser baixado: {model_path}")

# Carregar classes do JSON
if json_path.exists():
    with open(json_path, 'r', encoding='utf-8') as f:
        class_data = json.load(f)
else:
    raise FileNotFoundError(f"Erro: O arquivo JSON não foi encontrado: {json_path}")

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

    # Carregar pesos
    model.load_state_dict(torch.load(str(model_path), map_location=torch.device('cpu'), weights_only=False))
    model.eval()
    return model

def get_model():
    """Retorna o modelo carregado, usando cache para eficiência."""
    global _model
    if _model is None:
        _model = load_model()
    return _model

preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

def classify_image(image):
    """Recebe uma imagem PIL, faz a predição e retorna as 3 classes prováveis."""
    model = get_model()  # Usa modelo em cache
    image = preprocess(image).unsqueeze(0) 

    with torch.no_grad():  # Desativa cálculo de gradientes
        outputs = model(image)
        probabilities = torch.nn.functional.softmax(outputs, dim=1)[0]  # Probabilidades por classe
    
    # Pegando as 3 classes com maior probabilidade
    top_probs, top_catids = torch.topk(probabilities, 3)

    # Lista de resultados
    results = []
    for i in range(3):
        results.append({
            "scientific_name": class_names[top_catids[i].item()],
            "popular_name": class_populares[top_catids[i].item()],
            "link": class_links[top_catids[i].item()],
            "probability": f"{top_probs[i].item() * 100:.2f}%"
        })

    return results, top_probs[0].item() * 100

