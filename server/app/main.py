from fastapi import FastAPI
from app.routes.extract import router as extract_router

app = FastAPI(title="OCR & PDF Extraction API")
app.include_router(extract_router, prefix="/api")
