# backend/utils.py
import torch
from torchvision import transforms
from PIL import Image

# Define your class labels (adjust as per your training)
CLASSES = ['clear', 'rainy', 'dark']

# Transform pipeline (compatible with Pillow >=10.0.0)
transform = transforms.Compose([
    transforms.Resize((224, 224), interpolation=Image.Resampling.LANCZOS),
    transforms.ToTensor()
])

# Load model (make sure weather_model.pt exists)
try:
    model = torch.load("weather_model.pt", map_location=torch.device('cpu'))
    model.eval()
except Exception as e:
    print("Failed to load weather model:", e)
    model = None

def detect_weather(image_path):
    if model is None:
        return 'model_not_loaded'

    image = Image.open(image_path).convert('RGB')
    img_tensor = transform(image).unsqueeze(0)

    with torch.no_grad():
        output = model(img_tensor)
        _, predicted = torch.max(output, 1)
        return CLASSES[predicted.item()]
