import torch
from PIL import Image
import torchvision.transforms as T
import numpy as np
from .model_def import UNetGeneratorCBAM_Multimodal

def load_generator(model_path: str):
    model = UNetGeneratorCBAM_Multimodal()
    model.load_state_dict(torch.load(model_path, map_location=torch.device("cpu")))
    model.eval()
    return model

def run_inference(image: Image.Image, model) -> Image.Image:
    transform = T.Compose([
        T.Resize((256, 256)),
        T.ToTensor()
    ])
    x = transform(image).unsqueeze(0)
    z = torch.randn(1, 1, 256, 256)

    with torch.no_grad():
        output = model(x, z)[0]

    output_img = (output.clamp(0, 1).permute(1, 2, 0).numpy() * 255).astype(np.uint8)
    return Image.fromarray(output_img)

def run_inference_variants(image: Image.Image, model, count: int = 3):
    transform = T.Compose([
        T.Resize((256, 256)),
        T.ToTensor()
    ])
    x = transform(image).unsqueeze(0)
    variants = []

    with torch.no_grad():
        for _ in range(count):
            z = torch.randn(1, 1, 256, 256)
            output = model(x, z)[0]
            output_img = (output.clamp(0, 1).permute(1, 2, 0).numpy() * 255).astype(np.uint8)
            variants.append(Image.fromarray(output_img))

    return variants