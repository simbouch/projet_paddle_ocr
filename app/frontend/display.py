import streamlit as st
from PIL import Image
import io

def show_uploaded_file(uploaded_file, caption="Fichier téléchargé"):
    """
    Display uploaded file (image or PDF) in Streamlit
    
    Args:
        uploaded_file: Streamlit UploadedFile object
        caption: Display caption
    
    Returns:
        PIL Image or None if error
    """
    try:
        if uploaded_file.type.startswith('image/'):
            image = Image.open(uploaded_file)
            st.image(image, caption=caption, use_column_width=True)
            return image
        else:
            st.warning("Format de fichier non supporté")
            return None
    except Exception as e:
        st.error(f"Erreur d'ouverture: {str(e)}")
        return None