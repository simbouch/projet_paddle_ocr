import streamlit as st
from PIL import Image
import pandas as pd
from typing import List, Dict

def show_uploaded_file(uploaded_file, caption="Image téléchargée") -> Image.Image:
    """
    Ouvre et affiche l'image téléchargée dans Streamlit.
    """
    try:
        image = Image.open(uploaded_file)
        st.image(image, caption=caption, use_column_width=True)
        return image
    except Exception as e:
        st.error(f"Erreur lors de l'ouverture de l'image : {e}")
        return None

def display_ocr_results(text: str, metadata: List[Dict]) -> None:
    """
    Affiche les résultats OCR de manière améliorée.
    
    - Le texte extrait est affiché dans un bloc de code.
    - Les métadonnées (confiance, position) sont affichées dans un expander sous forme de tableau.
    """
    st.markdown("### Texte Extrait")
    st.code(text, language="text")
    
    with st.expander("Détails d'analyse OCR"):
        if metadata:
            df = pd.DataFrame(metadata)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("Aucune donnée de confiance disponible.")
