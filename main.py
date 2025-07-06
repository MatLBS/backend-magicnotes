from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import shutil
import uvicorn
import os
from ocr import process_image

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
    print("python")
    os.makedirs("temp_images", exist_ok=True)

    file_location = f"temp_images/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    print("Fichier sauvegardé à :", file_location)
    print("Taille du fichier sauvegardé :", os.path.getsize(file_location), "octets")

    highlighted_words = process_image(file_location)
    return highlighted_words

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)
