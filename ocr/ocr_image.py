from preprocess_image import *

def ocr_image(image_path, lang="eng"):
    """
    Process an image for OCR and extract text using Tesseract.
    Allows specifying the language ('eng' for English, 'ara' for Arabic, etc.).
    """
    try:
        logging.info("Preprocessing image: %s", image_path)
        processed_img = preprocess_image(image_path)
        # Convert the processed OpenCV image to a PIL image
        pil_img = Image.fromarray(processed_img)
        logging.info("Extracting text using Tesseract (language=%s)...", lang)
        # Run Tesseract OCR on the image, specifying the language.
        text = pytesseract.image_to_string(pil_img, lang=lang)
        return text
    except Exception as e:
        logging.error("An error occurred during OCR: %s", e)
        return None
