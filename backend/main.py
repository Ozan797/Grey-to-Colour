from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from io import BytesIO
from PIL import Image

from model.generator import load_generator, run_inference

app = FastAPI()

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load trained model
generator_model = load_generator("model.pth")

@app.post("/api/colourise-image")
async def colourise_image(file: UploadFile = File(...)):
    try:
        print("\n📥 Received request...")

        contents = await file.read()
        print("📸 Image bytes loaded")

        image = Image.open(BytesIO(contents)).convert("L")
        print("✅ Converted to grayscale")

        result = run_inference(image, generator_model)
        print("🎨 Model inference complete")

        buf = BytesIO()
        result.save(buf, format="PNG")
        buf.seek(0)
        print("🧴 Image saved to buffer")

        return StreamingResponse(buf, media_type="image/png")

    except Exception as e:
        print("❌ ERROR:", e)
        return JSONResponse(status_code=500, content={"error": str(e)})
