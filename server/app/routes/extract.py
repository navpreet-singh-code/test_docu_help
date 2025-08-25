import json
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from app.services.ocr_service import process_uploaded_file
from app.api.grok_integration import extract_fields_with_grok, identify_document_type_with_grok

router = APIRouter()

def load_grok_fields():
    with open("server/app/grok_fields.json", "r") as f:
        data = json.load(f)
        return data["fields"] 

@router.post("/extract")
async def extract_text(file: UploadFile = File(...)):
    try:
        extracted_text = await process_uploaded_file(file)
        # Identify document type
        doc_type = await identify_document_type_with_grok(extracted_text)
        # Extract fields
        fields = load_grok_fields()
        print('nobuuu',fields)
        parsed_data = await extract_fields_with_grok(extracted_text, fields)
        print('japan',parsed_data)
        return JSONResponse(content={
            "doc_type": doc_type,
            "extracted_text": extracted_text,
            "parsed_data": parsed_data
        })
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
