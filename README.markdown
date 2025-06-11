# Tesseract Professional OCR API

A robust and scalable Optical Character Recognition (OCR) API built with FastAPI, Tesseract OCR, and OpenCV. This project provides a production-ready solution for extracting text from images with advanced preprocessing capabilities and comprehensive error handling.

## Table of Contents

- Features
- Architecture
- Prerequisites
- Installation
- Configuration
- Running the Application
- API Endpoints
- Usage Examples
- Testing
- Project Structure
- Contributing
- Troubleshooting
- License

## Features

- **Text Extraction**: Extracts text from images (PNG, JPEG, BMP, TIFF) using Tesseract OCR.
- **Multi-language Support**: Supports multiple languages (e.g., 'eng' for English, 'ara' for Arabic).
- **Advanced Image Preprocessing**:
  - Grayscale conversion
  - Adaptive thresholding
  - Noise reduction
  - Image deskewing for improved text alignment
- **Robust API**:
  - Built with FastAPI for high performance
  - Interactive API documentation (Swagger UI and ReDoc)
  - Health check endpoint for monitoring
- **Configuration Management**: YAML-based configuration with environment variable support
- **Logging**: Structured logging with file and console output
- **Input Validation**: Strict file extension validation and request schema validation
- **Error Handling**: Comprehensive error handling with meaningful error messages
- **Testing**: Unit tests with pytest for reliability
- **Development Features**: Auto-reload for development and modular code structure

## Architecture

The project follows a modular architecture to ensure maintainability and scalability:

- **API Layer**: FastAPI-based REST API handling HTTP requests and responses
- **Core Layer**: Business logic for OCR processing and image preprocessing
- **Models Layer**: Pydantic schemas for request/response validation
- **Configuration**: YAML-based settings with Pydantic validation
- **Tests**: Unit tests for core functionality
- **Logging**: Centralized logging configuration for debugging and monitoring

## Prerequisites

- **Python**: Version 3.9 or higher
- **Tesseract OCR**: Must be installed on the system
- **System Dependencies**:
  - Windows: Tesseract installer
  - Linux: `tesseract-ocr` and `libtesseract-dev`
  - macOS: `tesseract` via Homebrew
- **Optional**: Virtual environment tool (e.g., `venv`, `virtualenv`)

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/your-username/ocr-api.git
   cd ocr-api
   ```

2. **Create a Virtual Environment** (recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   ```

3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Install Tesseract OCR**:

   - **Windows**: Download and install from Tesseract at UB Mannheim. Add Tesseract to your system PATH or specify the path in `config/settings.yaml`.
   - **Linux**:

     ```bash
     sudo apt-get update
     sudo apt-get install tesseract-ocr libtesseract-dev
     ```
   - **macOS**:

     ```bash
     brew install tesseract
     ```

5. **Verify Tesseract Installation**:

   ```bash
   tesseract --version
   ```

## Configuration

The application uses a YAML configuration file located at `config/settings.yaml`. You can also override settings using a `.env` file.

**Default** `config/settings.yaml`:

```yaml
app_name: OCR API
log_file: logs/ocr_api.log
temp_dir: temp
tesseract_cmd: tesseract
```

**Optional** `.env` **File**:

```bash
TESSERACT_CMD=/path/to/tesseract
TEMP_DIR=/custom/temp/path
LOG_FILE=/custom/log/path/ocr_api.log
```

To customize:

1. Modify `config/settings.yaml` directly, or
2. Create a `.env` file in the project root with overridden values.

Ensure the `temp_dir` and `log_file` directories exist or are writable. The application creates the `temp_dir` automatically if it doesn't exist.

## Running the Application

1. **Start the API**:

   ```bash
   python run.py
   ```

   This starts the FastAPI server on `http://localhost:3000` with auto-reload enabled for development.

2. **Access API Documentation**:

   - Swagger UI: `http://localhost:3000/docs`
   - ReDoc: `http://localhost:3000/redoc`

3. **Verify API Status**:

   ```bash
   curl http://localhost:3000/health
   ```

   Expected response:

   ```json
   {"status": "healthy", "version": "1.0.0"}
   ```

## API Endpoints

| Endpoint | Method | Description | Parameters |
| --- | --- | --- | --- |
| `/ocr` | POST | Extracts text from an uploaded image | \- `file`: Image file (PNG, JPEG, BMP, TIFF)<br>- `language`: Language code (default: 'eng') |
| `/health` | GET | Checks API health status | None |

**Request Example for** `/ocr`:

```bash
curl -X POST "http://localhost:3000/ocr" \
     -F "file=@sample.png" \
     -F "language=eng"
```

**Response Example (Success)**:

```json
{
  "status": "success",
  "extracted_text": "Sample text from image",
  "error": null
}
```

**Response Example (Error)**:

```json
{
  "status": "error",
  "extracted_text": null,
  "error": "Unsupported file extension. Allowed: .png, .jpg, .jpeg, .bmp, .tiff"
}
```

## Usage Examples

### Using cURL

```bash
curl -X POST "http://localhost:3000/ocr" \
     -F "file=@/path/to/image.png" \
     -F "language=ara"
```

### Using Python (requests)

```python
import requests

url = "http://localhost:3000/ocr"
files = {"file": open("sample.png", "rb")}
data = {"language": "eng"}
response = requests.post(url, files=files, data=data)
print(response.json())
```

### Supported Languages

Tesseract supports multiple languages. Common language codes:

- `eng`: English
- `ara`: Arabic
- `fra`: French
- `deu`: German
- `spa`: Spanish Check Tesseract documentation for the full list of supported languages.

## Testing

The project includes unit tests using pytest.

1. **Run Tests**:

   ```bash
   pytest tests/ -v
   ```

2. **Test Coverage**: To generate a coverage report:

   ```bash
   pytest tests/ --cov=src --cov-report=html
   ```

   The coverage report will be generated in the `htmlcov/` directory.

**Note**: Some tests may require sample images. Update `tests/test_ocr.py` with actual test images for comprehensive testing.

## Project Structure

```
ocr-api/
├── src/
│   ├── api/
│   │   └── main.py              # FastAPI application and endpoints
│   ├── core/
│   │   ├── config.py            # Configuration management
│   │   ├── ocr_processor.py     # OCR processing logic
│   │   └── image_preprocessor.py # Image preprocessing logic
│   ├── models/
│   │   └── schemas.py           # Pydantic models for request/response
├── tests/
│   └── test_ocr.py              # Unit tests
├── config/
│   └── settings.yaml            # Configuration file
├── requirements.txt              # Python dependencies
├── run.py                       # Application entry point
├── README.md                    # Project documentation
└── .env                         # Optional environment variables
```

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m "Add your feature"`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Create a Pull Request

**Coding Guidelines**:

- Follow PEP 8 style guidelines
- Include type hints
- Add unit tests for new features
- Update documentation as needed

## Troubleshooting

- **Tesseract Not Found**:
  - Verify Tesseract is installed and accessible in your PATH
  - Update `TESSERACT_CMD` in `config/settings.yaml` or `.env`
- **Image Processing Fails**:
  - Ensure the image file is valid and not corrupted
  - Check if the file format is supported (PNG, JPEG, BMP, TIFF)
- **Permission Errors**:
  - Ensure write permissions for `temp_dir` and `log_file` directories
- **Dependency Issues**:
  - Verify all dependencies are installed (`pip install -r requirements.txt`)
  - Use a virtual environment to avoid conflicts

For additional help, open an issue on the repository or check the logs in the configured `log_file`.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
