FROM python:3.12-slim

# Install system deps for PyMuPDF, Tesseract, OpenCV
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download spaCy base model
RUN python -m spacy download en_core_web_lg

COPY . .

EXPOSE 8000
