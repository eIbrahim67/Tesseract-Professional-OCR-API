from preprocess_image import *
from ocr_image import ocr_image

if __name__ == "__main__":
    # Specify the image path and language code
    image_path = "../src/test_ara_1.png"  # Replace with your image file (for Arabic, for example)
    language = "ara"  # Set 'ara' for Arabic; change to 'eng' for English if needed

    logging.info("Starting OCR process for %s", image_path)
    extracted_text = ocr_image(image_path, lang=language)

    if extracted_text is not None:
        logging.info("OCR extraction completed successfully.")
        print("Extracted Text:")
        print(extracted_text)
    else:
        logging.error("OCR extraction failed.")