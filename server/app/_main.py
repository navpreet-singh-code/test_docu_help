# main.py

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from pdf2image import convert_from_bytes
from PIL import Image
import pdfplumber
import io
import easyocr

# Create FastAPI app
app = FastAPI(title="OCR and PDF Extraction API with EasyOCR")

# Create EasyOCR reader (English by default)
reader = easyocr.Reader(['en'], gpu=False)

@app.post("/extract")
async def extract_text(file: UploadFile = File(...)):
    # Check if file type is supported
    if not (
        file.content_type.startswith("image/") or
        file.content_type == "application/pdf"
    ):
        raise HTTPException(status_code=400, detail="Unsupported file type.")

    content = await file.read()
    results = []

    # 1️⃣ Handle Images
    if file.content_type.startswith("image/"):
        image = Image.open(io.BytesIO(content))
        text_lines = reader.readtext(np.array(image), detail=0)
        text_result = "\n".join(text_lines)
        results.append({
            "method": "ocr",
            "page": 1,
            "text": text_result.strip()
        })

    # 2️⃣ Handle PDFs
    elif file.content_type == "application/pdf":
        text_based = False
        text_content = ""

        # Try direct text extraction with pdfplumber
        with pdfplumber.open(io.BytesIO(content)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text() or ""
                if page_text.strip():
                    text_based = True
                text_content += page_text.strip() + "\n"

        if text_based:
            # Text-based PDF
            results.append({
                "method": "direct",
                "text": text_content.strip()
            })
        else:
            # Image-based PDF, requires OCR
            images = convert_from_bytes(content)
            for i, image in enumerate(images):
                text_lines = reader.readtext(np.array(image), detail=0)
                text_result = "\n".join(text_lines)
                results.append({
                    "method": "ocr",
                    "page": i + 1,
                    "text": text_result.strip()
                })

    return JSONResponse(content={"extracted_text": results})