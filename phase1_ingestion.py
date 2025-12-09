from fastapi import UploadFile
import fitz
from PIL import Image
import pytesseract
import re
import os
import base64
import tempfile

# Linux Tesseract Path
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"


# -----------------------------------
# Detect file type
# -----------------------------------
def is_txt(filename: str):
    return filename.lower().endswith(".txt")


# -----------------------------------
# OCR + PDF Text & Image Extraction
# -----------------------------------
def extract_text_and_images_from_pdf(path):
    doc = fitz.open(path)
    full_text = ""
    images = []

    for page_num, page in enumerate(doc):

        # PDF digital text
        text = page.get_text()
        full_text += text + "\n"

        # OCR fallback
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        ocr_text = pytesseract.image_to_string(img)
        full_text += ocr_text + "\n"

        # Extract embedded images
        for img_index, img_dict in enumerate(page.get_images(full=True)):
            xref = img_dict[0]
            base_image = doc.extract_image(xref)
            img_bytes = base_image["image"]
            img_b64 = base64.b64encode(img_bytes).decode("utf-8")

            images.append({
                "page": page_num + 1,
                "image_index": img_index + 1,
                "image_base64": img_b64
            })

    return full_text, images


# -----------------------------------
# TXT extraction
# -----------------------------------
async def extract_text_from_txt(file: UploadFile):
    content = (await file.read()).decode("utf-8", errors="ignore")
    return content, []


# -----------------------------------
# PII Masking
# -----------------------------------
def mask_pii(text):
    text = re.sub(r'\S+@\S+', '[EMAIL]', text)
    text = re.sub(r'\b\d{10}\b', '[PHONE]', text)
    text = re.sub(r'\b[A-Z][a-z]+ [A-Z][a-z]+\b', '[NAME]', text)
    text = re.sub(r'\d{1,5} [A-Za-z ]+', '[ADDRESS]', text)
    return text


# -----------------------------------
# Text Cleaning
# -----------------------------------
def clean_text(text):
    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r'Page \d+', '', text)
    text = re.sub(r'\s{2,}', ' ', text)
    return text.strip()


# -----------------------------------
# Chunking
# -----------------------------------
def group_content(text, max_chars=500):
    text = text.strip()
    chunks = []

    while len(text) > max_chars:
        pos = text.rfind("\n", 0, max_chars)
        if pos == -1:
            pos = max_chars
        chunk = text[:pos].strip()
        chunks.append(chunk)
        text = text[pos:].strip()

    if text:
        chunks.append(text)

    return chunks


# -----------------------------------
# Main ingestion orchestrator
# -----------------------------------
async def process_document(file: UploadFile):

    # Handle TXT directly
    if is_txt(file.filename):
        raw_text, images = await extract_text_from_txt(file)

    else:
        # Store PDF temporarily
        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, file.filename)

        with open(temp_path, "wb") as f:
            f.write(await file.read())

        raw_text, images = extract_text_and_images_from_pdf(temp_path)
        os.remove(temp_path)

    anonymized = mask_pii(raw_text)
    cleaned = clean_text(anonymized)
    content_groups = group_content(cleaned, max_chars=500)

    return {
        "content_groups": content_groups,
        "images": images
    }
