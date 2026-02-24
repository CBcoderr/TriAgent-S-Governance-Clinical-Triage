import fitz
import pytesseract
from PIL import Image
import re
import os

# 🔥 SET THIS TO YOUR TESSERACT INSTALL PATH (Windows)
tesseract_path = os.getenv("TESSERACT_PATH")

if tesseract_path:
    pytesseract.pytesseract.tesseract_cmd = tesseract_path


def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text


def extract_text_from_image(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text


def parse_lab_values(text):
    text = text.lower()

    labs_found = []

    spo2_match = re.search(r"spo2\s*[:\-]?\s*(\d+)", text)
    hr_match = re.search(r"(heart rate|hr)\s*[:\-]?\s*(\d+)", text)

    if spo2_match:
        labs_found.append(f"SpO2 {spo2_match.group(1)}")

    if hr_match:
        labs_found.append(f"HR {hr_match.group(2)}")

    return " ".join(labs_found) if labs_found else ""
