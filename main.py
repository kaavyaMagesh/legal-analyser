from fastapi import FastAPI, UploadFile, File
import fitz
from PIL import Image
import pytesseract
import re
import os
import base64
import tempfile

# -------------- Tesseract Path (Windows) --------------
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

app = FastAPI()

# -----------------------------
# OCR + Text + Image Extraction
# -----------------------------
def extract_text_and_images(path):
    doc = fitz.open(path)
    full_text = ""
    images = []

    for page_num, page in enumerate(doc):
        # 1️⃣ Extract text from digital PDFs
        text = page.get_text()
        full_text += text + "\n"

        # 2️⃣ OCR for scanned PDFs
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        ocr_text = pytesseract.image_to_string(img)
        full_text += ocr_text + "\n"

        # 3️⃣ Extract embedded images
        for img_index, img_dict in enumerate(page.get_images(full=True)):
            xref = img_dict[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_b64 = base64.b64encode(image_bytes).decode("utf-8")
            images.append({
                "page": page_num + 1,
                "image_index": img_index + 1,
                "image_base64": image_b64
            })

    return full_text, images

# -----------------------------
# PII Masking
# -----------------------------
def mask_pii(text):
    text = re.sub(r'\S+@\S+', '[EMAIL]', text)
    text = re.sub(r'\b\d{10}\b', '[PHONE]', text)
    text = re.sub(r'\b[A-Z][a-z]+ [A-Z][a-z]+\b', '[NAME]', text)
    text = re.sub(r'\d{1,5} [A-Za-z ]+', '[ADDRESS]', text)
    return text

# -----------------------------
# Text Cleaning
# -----------------------------
def clean_text(text):
    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r'Page \d+', '', text)
    text = re.sub(r'\s{2,}', ' ', text)
    return text.strip()

# -----------------------------
# Simple content grouping
# -----------------------------
def group_content(text, max_chars=500):
    """Split text into chunks of roughly max_chars length."""
    text = text.strip()
    chunks = []
    while len(text) > max_chars:
        # Try to split at the last newline before max_chars
        split_pos = text.rfind("\n", 0, max_chars)
        if split_pos == -1:
            split_pos = max_chars
        chunk = text[:split_pos].strip()
        chunks.append(chunk)
        text = text[split_pos:].strip()
    if text:
        chunks.append(text)
    return chunks

# -----------------------------
# FastAPI Endpoints
# -----------------------------
@app.get("/")
def root():
    return {"message": "Backend live"}

@app.post("/process")
async def process_document(file: UploadFile = File(...)):
    # Use Windows-safe temp path
    temp_dir = tempfile.gettempdir()
    temp_path = os.path.join(temp_dir, file.filename)

    # Save uploaded file
    with open(temp_path, "wb") as f:
        f.write(await file.read())

    # Extract text + images
    raw_text, images = extract_text_and_images(temp_path)

    # Mask PII
    anonymized = mask_pii(raw_text)

    # Clean text
    cleaned = clean_text(anonymized)

    # Group content into chunks
    content_groups = group_content(cleaned, max_chars=500)

    # Delete temp file
    os.remove(temp_path)

    return {
        "content_groups": content_groups,
        "images": images  # base64-encoded images
    }
