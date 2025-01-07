import torch
import json
import torchvision.transforms as transforms
from torchvision import models

json_path = r"new_names.json"

with open(json_path, 'r', encoding='utf-8') as f:
    class_data = json.load(f)

# colocando em ordem alfabetica já que ao realizar o treinamento esse metodo foi usado
sorted_class_data = sorted(class_data.items(), key=lambda x: x[1]["nomes_cientificos"][0])

# exraindo as informações e mantendo na ordem alfabética
class_names = [data[1]["nomes_cientificos"][0] for data in sorted_class_data]
class_populares = [data[1]["nomes_populares"][0] for data in sorted_class_data]
class_links = [data[1]["link"] for data in sorted_class_data]

num_classes = len(class_names)

# Carregando o modelo ResNet50 
model = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V1)
num_ftrs = model.fc.in_features
model.fc = torch.nn.Linear(num_ftrs, num_classes)# ajusta com as classes
model.load_state_dict(torch.load("webapp\model\pesos_it_1.pth", weights_only=True, map_location=torch.device('cpu')))# pesos do modelo 
model.eval()# modo de avaliação do modelo

preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# Função classifica imagem
def classify_image(image):
    image = preprocess(image).unsqueeze(0)
    with torch.no_grad(): # sem calcular gradientes
        outputs = model(image) 
        probabilities = torch.nn.functional.softmax(outputs, dim=1)[0] # probabilidade de cada classe
        # definindo classe com maior probabilidade
        top_prob, top_catid = torch.max(probabilities, 0)
    
    # extraindo as informações
    scientific_name = class_names[top_catid.item()]
    popular_name = class_populares[top_catid.item()]
    link = class_links[top_catid.item()]
    prob = top_prob.item() * 100 
    
    # formatação do resultado
    result = f"Nome Científico: {scientific_name}\n"
    result += f"Nome Popular: {popular_name}\n"
    result += f"Link: {link}\n"
    result += f"Probabilidade: {prob:.2f}%\n"
    
    return result
