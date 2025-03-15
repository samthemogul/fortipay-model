import torch
import torchvision.transforms as transforms
from PIL import Image
from timm import create_model

# Load pre-trained ResNet model
model = create_model("resnet50", pretrained=True, num_classes=0)
model.eval()

def extract_features(image_path):
    img = Image.open(image_path).convert("RGB")
    transform = transforms.Compose([transforms.Resize((224, 224)), transforms.ToTensor()])
    img_tensor = transform(img).unsqueeze(0)

    with torch.no_grad():
        features = model(img_tensor)
    return features.numpy()
