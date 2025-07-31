import torch
from torchvision import transforms
from PIL import Image

# Load pre-trained PyTorch model
model = torch.load("weather_model.pt", map_location=torch.device('cpu'))
model.eval()

# Define your class labels
classes = ['rainy', 'dark', 'clear']

# Define preprocessing pipeline
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

def detect_weather(image_path):
    image = Image.open(image_path).convert("RGB")
    input_tensor = transform(image).unsqueeze(0)
    
    with torch.no_grad():
        output = model(input_tensor)
        pred_class = output.argmax(1).item()
    
    return classes[pred_class]
