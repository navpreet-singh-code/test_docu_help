from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from app.services.ocr_service import process_uploaded_file

router = APIRouter()

@router.post("/extract")
async def extract_text(file: UploadFile = File(...)):
    try:
        result = await process_uploaded_file(file)
        return JSONResponse(content={"extracted_text": result})
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
