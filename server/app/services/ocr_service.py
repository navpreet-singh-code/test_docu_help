import easyocr
import pdfplumber
from pdf2image import convert_from_bytes
from PIL import Image
import numpy as np
import io
from app.utils.file_utils import is_supported_file_type, is_image_type

reader = easyocr.Reader(['en'], gpu=False)

async def process_uploaded_file(file):
    if not is_supported_file_type(file.content_type):
        raise ValueError("Unsupported file type")

    content = await file.read()
    results = []

    if is_image_type(file.content_type):
        image = Image.open(io.BytesIO(content))
        text_lines = reader.readtext(np.array(image), detail=0)
        results.append({"method": "ocr", "page": 1, "text": "\n".join(text_lines).strip()})

    elif file.content_type == "application/pdf":
        with pdfplumber.open(io.BytesIO(content)) as pdf:
            direct_text = ""
            text_found = False
            for page in pdf.pages:
                extracted = page.extract_text() or ""
                if extracted.strip():
                    text_found = True
                direct_text += extracted.strip() + "\n"

        if text_found:
            results.append({"method": "direct", "text": direct_text.strip()})
        else:
            images = convert_from_bytes(content)
            for i, image in enumerate(images):
                text_lines = reader.readtext(np.array(image), detail=0)
                results.append({"method": "ocr", "page": i + 1, "text": "\n".join(text_lines).strip()})

    return results
