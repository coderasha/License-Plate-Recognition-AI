import easyocr
import cv2
import torch
from torchvision import transforms
from PIL import Image

reader = easyocr.Reader(['en'])

def detect_text(image_path):
    results = reader.readtext(image_path)
    if not results:
        return "No plate detected"
    return max(results, key=lambda x: x[2])[1]

def detect_weather(image_path):
    model = torch.load("weather_model.pt", map_location=torch.device('cpu'))
    model.eval()

    image = Image.open(image_path).convert("RGB")
    image = image.resize((224, 224), Image.Resampling.LANCZOS)  # fixed ANTIALIAS
    transform = transforms.Compose([
        transforms.ToTensor(),
    ])
    input_tensor = transform(image).unsqueeze(0)

    with torch.no_grad():
        outputs = model(input_tensor)
        _, predicted = torch.max(outputs.data, 1)

    label_map = {
        0: 'Clear',
        1: 'Rainy',
        2: 'Foggy',
        3: 'Dark',
        4: 'Cloudy'
    }
    return label_map.get(predicted.item(), "Unknown")
