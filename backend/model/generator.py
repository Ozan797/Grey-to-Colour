import torch
from PIL import Image
import torchvision.transforms as T
import numpy as np
from .model_def import UNetGeneratorCBAM_Multimodal

def load_generator(model_path: str):
    """Load the trained generator model from a .pth file."""
    model = UNetGeneratorCBAM_Multimodal()
    model.load_state_dict(torch.load(model_path, map_location=torch.device("cpu")))
    model.eval()
    return model

def run_inference(image: Image.Image, model) -> Image.Image:
    """Run inference on a single grayscale image using the trained GAN."""
    transform = T.Compose([
        T.Resize((256, 256)),  # match training resolution
        T.ToTensor()
    ])
    x = transform(image).unsqueeze(0)  # Shape: [1, 1, 256, 256]
    z = torch.randn(1, 1, 256, 256)     # Random latent noise input

    with torch.no_grad():
        output = model(x, z)[0]         # Output shape: [3, 256, 256]

    output_img = (output.clamp(0, 1).permute(1, 2, 0).numpy() * 255).astype(np.uint8)
    return Image.fromarray(output_img)
