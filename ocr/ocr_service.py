import cv2
import pytesseract
import logging
from PIL import Image
import numpy as np
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Set Tesseract path from environment variable
TESSERACT_CMD = os.getenv("TESSERACT_PATH", r"C:\Program Files\Tesseract-OCR\tesseract.exe")
pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD

def preprocess_image(image_path: str) -> np.ndarray:
    """
    Preprocess the image to improve OCR accuracy:
    - Load image using OpenCV.
    - Resize to ensure consistent DPI.
    - Convert to grayscale.
    - Apply noise reduction and adaptive thresholding.
    """
    try:
        image = cv2.imread(image_path)
        if image is None:
            raise FileNotFoundError(f"Image not found: {image_path}")

        # Resize image to ensure consistent DPI (300 DPI equivalent)
        scale_percent = 300 / 72  # Assuming 72 DPI as base
        width = int(image.shape[1] * scale_percent)
        height = int(image.shape[0] * scale_percent)
        image = cv2.resize(image, (width, height), interpolation=cv2.INTER_CUBIC)

        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Apply adaptive thresholding
        thresh = cv2.adaptiveThreshold(
            blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )

        return thresh
    except Exception as e:
        logger.error(f"Error in preprocessing image {image_path}: {str(e)}")
        raise

def ocr_image(image_path: str, lang: str = "eng") -> str:
    """
    Process an image for OCR and extract text using Tesseract.
    Args:
        image_path: Path to the image file.
        lang: Language code for OCR (e.g., 'eng', 'ara').
    Returns:
        Extracted text or None if an error occurs.
    """
    try:
        logger.info(f"Preprocessing image: {image_path}")
        processed_img = preprocess_image(image_path)

        # Convert OpenCV image to PIL for Tesseract
        pil_img = Image.fromarray(processed_img)

        logger.info(f"Extracting text using Tesseract (language={lang})...")
        # Configure Tesseract with custom options
        custom_config = f"--oem 3 --psm 6 -l {lang}"
        text = pytesseract.image_to_string(pil_img, config=custom_config)

        if not text.strip():
            logger.warning("No text extracted from the image.")
            return None

        return text
    except Exception as e:
        logger.error(f"Error during OCR: {str(e)}")
        return None