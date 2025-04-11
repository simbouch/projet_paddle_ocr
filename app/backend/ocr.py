from paddleocr import PaddleOCR
import cv2
import numpy as np
from PIL import Image
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize PaddleOCR once (lazy loading)
_ocr_instance = None

def get_ocr_instance():
    global _ocr_instance
    if _ocr_instance is None:
        _ocr_instance = PaddleOCR(
            lang="fr",
            use_angle_cls=True,
            show_log=False  # Disable verbose logging
        )
    return _ocr_instance

def perform_ocr(image: Image.Image) -> str:
    """
    Perform OCR on a PIL Image using PaddleOCR
    
    Args:
        image: PIL Image to process
    
    Returns:
        Extracted text as a single string
    """
    try:
        # Convert PIL Image to OpenCV format (BGR)
        img_array = np.array(image)
        if len(img_array.shape) == 2:  # Grayscale
            img_array = cv2.cvtColor(img_array, cv2.COLOR_GRAY2BGR)
        else:  # RGB
            img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
        
        # Get OCR instance and process image
        ocr = get_ocr_instance()
        result = ocr.ocr(img_array, cls=True)
        
        # Extract and concatenate text
        extracted_text = []
        if result and result[0]:
            for line in result[0]:
                if line and len(line) >= 2:
                    text = line[1][0]
                    if text.strip():
                        extracted_text.append(text.strip())
        
        return "\n".join(extracted_text) if extracted_text else "Aucun texte détecté."
    
    except Exception as e:
        logger.error(f"OCR failed: {str(e)}")
        return f"Erreur OCR: {str(e)}"