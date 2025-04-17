from model.model_def import UNetGeneratorCBAM_Multimodal
import torch

# Load model
model = UNetGeneratorCBAM_Multimodal()
model.load_state_dict(torch.load("model.pth", map_location="cpu"))
model.eval()

# Create dummy inputs at 256x256 resolution
x = torch.randn(1, 1, 256, 256)  # Grayscale input
z = torch.randn(1, 1, 256, 256)  # Noise input

# Run forward pass
with torch.no_grad():
    output = model(x, z)

print("✅ Output shape:", output.shape)
