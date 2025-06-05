# OCR API Service

A professional OCR (Optical Character Recognition) API built with FastAPI and Tesseract OCR, designed for extracting text from images in web and mobile applications.

## Features
- Supports multiple image formats (PNG, JPEG, BMP, TIFF).
- Configurable language support (e.g., `eng` for English, `ara` for Arabic).
- Advanced image preprocessing for improved OCR accuracy.
- FastAPI-based endpoint with OpenAPI documentation.
- Environment variable configuration for Tesseract path.

## Prerequisites
- Python 3.8+
- Tesseract OCR installed on the server (e.g., `/usr/bin/tesseract` on Linux or `C:\Program Files\Tesseract-OCR\tesseract.exe` on Windows).
- Tesseract language data files for desired languages (e.g., `eng`, `ara`).

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the `.env` file with the Tesseract path:
   ```plaintext
   TESSERACT_PATH=/path/to/tesseract
   ```

5. Run the API:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

## Usage
- Access the API at `http://localhost:8000`.
- Use the `/ocr` endpoint via a POST request with a multipart form:
  - `file`: The image file to process.
  - `language`: Optional language code (default: `eng`).

Example using `curl`:
```bash
curl -X POST "http://localhost:8000/ocr?language=eng" -F "file=@/path/to/image.png"
```

Example response:
```json
{
  "status": "success",
  "extracted_text": "Extracted text from the image",
  "error": null
}
```

- Explore the interactive API documentation at `http://localhost:8000/docs`.

## Deployment
- Deploy on a cloud platform like AWS, Google Cloud, or Heroku.
- Ensure Tesseract and language data files are installed on the server.
- Use a reverse proxy (e.g., Nginx) for production.
- Secure the endpoint with authentication if needed (e.g., OAuth2).

## Notes
- Supported languages depend on installed Tesseract language packs.
- Preprocessing includes resizing, noise reduction, and adaptive thresholding for better OCR results.
- Temporary files are automatically cleaned up after processing.

## License
MIT License