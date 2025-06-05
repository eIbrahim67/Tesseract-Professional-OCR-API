import uvicorn
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import logging
from ocr_service import ocr_image
from pydantic import BaseModel
import os
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(
    title="OCR API",
    description="API for extracting text from images using Tesseract OCR",
    version="1.0.0"
)

class OCRRequest(BaseModel):
    language: Optional[str] = "eng"

class OCRResponse(BaseModel):
    extracted_text: Optional[str]
    status: str
    error: Optional[str]

ALLOWED_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.bmp', '.tiff'}

@app.post("/ocr", response_model=OCRResponse)
async def ocr_endpoint(file: UploadFile = File(...), language: str = "eng"):
    """
    Endpoint to perform OCR on an uploaded image.
    Args:
        file: Uploaded image file (PNG, JPEG, BMP, TIFF).
        language: Language code for OCR (default: 'eng').
    Returns:
        JSON response with extracted text or error message.
    """
    try:
        # Validate file extension
        ext = os.path.splitext(file.filename)[1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(status_code=400, detail=f"Unsupported file extension. Allowed: {ALLOWED_EXTENSIONS}")

        # Save uploaded file temporarily
        temp_file_path = f"temp_{file.filename}"
        with open(temp_file_path, "wb") as temp_file:
            temp_file.write(await file.read())

        # Perform OCR
        logger.info(f"Processing OCR for file: {file.filename}, language: {language}")
        extracted_text = ocr_image(temp_file_path, lang=language)

        # Clean up temporary file
        os.remove(temp_file_path)

        if extracted_text is None:
            return JSONResponse(
                status_code=500,
                content={"status": "error", "error": "OCR processing failed", "extracted_text": None}
            )

        return OCRResponse(
            status="success",
            extracted_text=extracted_text.strip(),
            error=None
        )

    except Exception as e:
        logger.error(f"Error during OCR processing: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"status": "error", "error": str(e), "extracted_text": None}
        )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)