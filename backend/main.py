from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from io import BytesIO
from PIL import Image
import base64

from model.generator import load_generator, run_inference_variants

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

generator_model = load_generator("model.pth")

@app.post("/api/colourise-image")
async def colourise_image(file: UploadFile = File(...), variation_strength: float = Form(2.5)):
    try:
        image = Image.open(BytesIO(await file.read())).convert("L")
        variants = run_inference_variants(image, generator_model, count=3, scale=variation_strength)
        images_base64 = []
        for img in variants:
            buf = BytesIO()
            img.save(buf, format="PNG")
            img_bytes = base64.b64encode(buf.getvalue()).decode("utf-8")
            images_base64.append(f"data:image/png;base64,{img_bytes}")
        return {"images": images_base64}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
