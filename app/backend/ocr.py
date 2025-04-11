import cv2
import numpy as np
from PIL import Image
import logging
from paddleocr import PaddleOCR
from typing import Tuple, List, Dict

logger = logging.getLogger(__name__)

_ocr_instance = None

def get_ocr_instance() -> PaddleOCR:
    global _ocr_instance
    if _ocr_instance is None:
        _ocr_instance = PaddleOCR(
            lang="fr",            # Utilisez "fr" pour le français (ajustez si besoin)
            use_angle_cls=True,
            show_log=False,
            drop_score=0.5        # Filtre pour ignorer les résultats à faible confiance
        )
    return _ocr_instance

def perform_ocr(image: Image.Image) -> Tuple[str, List[Dict]]:
    """
    Effectue l'OCR sur une image PIL en utilisant PaddleOCR et renvoie le texte extrait et les métadonnées.

    Retourne:
        (texte_extrait, metadata) où metadata est une liste de dictionnaires avec les informations (texte, confiance, position).
    """
    try:
        img_array = np.array(image)
        if len(img_array.shape) == 2:
            img_array = cv2.cvtColor(img_array, cv2.COLOR_GRAY2BGR)
        else:
            img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
        
        ocr = get_ocr_instance()
        result = ocr.ocr(img_array, cls=True)
        
        extracted_text = []
        text_metadata = []
        
        if result and result[0]:
            for line in result[0]:
                if line and len(line) >= 2:
                    text, conf = line[1]
                    if text.strip():
                        extracted_text.append(text.strip())
                        text_metadata.append({
                            "text": text.strip(),
                            "confidence": float(conf),
                            "position": [tuple(map(float, point)) for point in line[0]]
                        })
        
        return (
            "\n".join(extracted_text) if extracted_text else "Aucun texte détecté.",
            text_metadata
        )
    
    except Exception as e:
        logger.error(f"OCR Error: {str(e)}")
        return f"Erreur OCR: {str(e)}", []
