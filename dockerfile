FROM python:3.11-slim

# Installer Tesseract OCR
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    && apt-get clean

# Installer les dépendances Python
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

# Config Render
ENV PORT=10000
EXPOSE 10000

# Lancer ton backend (à adapter si ton fichier ≠ main.py)
CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--port=10000"]