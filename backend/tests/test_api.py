import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from PIL import Image
from io import BytesIO

from main import app

client = TestClient(app)

def create_dummy_image(size=(256, 256)):
    img = Image.new("L", size, color=128)
    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf

def test_colourise_success():
    print("\n🧪 Testing valid image upload...")
    response = client.post(
        "/api/colourise-image",
        files={"file": ("dummy.png", create_dummy_image(), "image/png")}
    )
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"
    print("✅ Passed: Valid image returns PNG output.")

def test_colourise_missing_file():
    print("\n🧪 Testing missing file case...")
    response = client.post("/api/colourise-image", files={})
    assert response.status_code == 422
    print("✅ Passed: Missing file returns 422 error.")

def test_colourise_wrong_filetype():
    print("\n🧪 Testing invalid filetype...")
    fake_text = BytesIO(b"not an image")
    response = client.post(
        "/api/colourise-image",
        files={"file": ("fake.txt", fake_text, "text/plain")}
    )
    assert response.status_code in [400, 500]
    print("✅ Passed: Invalid filetype handled properly.")
