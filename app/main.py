import streamlit as st
from paddleocr import PaddleOCR
import numpy as np
from PIL import Image

# Initialize PaddleOCR once
@st.cache_resource
def get_ocr():
    return PaddleOCR(
        lang='fr',
        use_angle_cls=True,
        show_log=False  # Disable internal logging
    )

def main():
    st.set_page_config(
        page_title="OCR Français Simple",
        page_icon="📄",
        layout="centered"
    )
    
    st.title("📄 OCR Français Simple")
    st.write("Téléchargez une image pour extraire le texte")

    uploaded_file = st.file_uploader(
        "Choisir une image",
        type=["png", "jpg", "jpeg"],
        accept_multiple_files=False
    )

    if uploaded_file is not None:
        try:
            # Display image
            image = Image.open(uploaded_file)
            st.image(image, caption="Image téléchargée", use_column_width=True)

            # Convert to OpenCV format
            img_array = np.array(image.convert('RGB'))
            
            # Perform OCR
            with st.spinner('Extraction du texte en cours...'):
                ocr = get_ocr()
                result = ocr.ocr(img_array, cls=True)
                
                # Extract text
                texts = []
                if result:
                    for line in result[0]:
                        if line and len(line) >= 2:
                            text = line[1][0].strip()
                            if text:
                                texts.append(text)
                
                # Display results
                if texts:
                    st.success("Texte extrait avec succès:")
                    st.write("\n".join(texts))
                else:
                    st.info("Aucun texte détecté dans l'image")

        except Exception as e:
            st.error(f"Erreur: {str(e)}")

if __name__ == "__main__":
    main()