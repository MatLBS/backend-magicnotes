from fastapi import FastAPI, File, UploadFile, Body
from fastapi.middleware.cors import CORSMiddleware
import shutil
import uvicorn
import os
from ocr import process_image, process_summary
from PIL import Image
import time

port = int(os.environ.get("PORT", 8000))

app = FastAPI()

# Permet à ton app React Native d’accéder à l’API
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
    os.makedirs("temp_images", exist_ok=True)

    file_location = f"temp_images/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    t1 = time.time()
    img = Image.open("temp_images/" + file.filename)
    img = img.convert("RGB")
    img.save(("temp_images/" + file.filename), "JPEG", optimize=True, quality=70)

    print("Fichier sauvegardé à :", file_location)
    print("Taille du fichier sauvegardé :", os.path.getsize(file_location), "octets")

    highlighted_words = process_image(file_location)
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
    print(summary)
    return summary


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=port)
