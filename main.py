from fastapi import FastAPI, File, UploadFile, Body
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from ocr import process_image, process_summary
from PIL import Image
import time
import base64
from io import BytesIO

port = int(os.environ.get("PORT", 8000))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/uploadImage")
async def upload_image(file: UploadFile = File(...)):
    print("-------------------python-------------------")
    t0 = time.time()

    # Lire l'image en mémoire
    image_bytes = await file.read()

    # Convertir et optimiser l'image en mémoire
    img = Image.open(BytesIO(image_bytes))
    img = img.convert("RGB")

    # Sauvegarder l'image optimisée dans un buffer en mémoire
    buffer = BytesIO()
    img.save(buffer, "JPEG", optimize=True, quality=70)
    buffer.seek(0)

    # Encoder en base64
    base64_image = base64.b64encode(buffer.read()).decode("utf-8")

    t1 = time.time()

    highlighted_words = process_image(base64_image)
    t2 = time.time()
    print("Temps OCR :", t2-t1)
    print("Temps total :", t2-t0)
    return highlighted_words

@app.post("/generateSummary")
async def generate_summary(notes: str = Body(...)):
    print("-------------------python-------------------")
    t0 = time.time()
    summary = process_summary(notes)
    t1 = time.time()
    print("Temps Génération Résumé :", t1-t0)
    return summary

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=port)
