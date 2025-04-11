import streamlit as st
from backend.ocr import perform_ocr
from frontend.display import show_uploaded_file, display_ocr_results

def main():
    st.set_page_config(
        page_title="Paddle OCR 2",
        page_icon="🔍",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("🔍 Paddle OCR 2")
    st.markdown("Cette application utilise PaddleOCR pour extraire le texte d'une image en français.")
    
    # Zone de chargement de l'image
    uploaded_file = st.file_uploader("Glissez-déposez ou sélectionnez une image (PNG, JPG, JPEG)", type=["png", "jpg", "jpeg"], label_visibility="hidden")
    
    # Bouton pour réinitialiser l'application
    if st.button("Réinitialiser"):
        st.experimental_rerun()
    
    if uploaded_file:
        col1, col2 = st.columns(2, gap="large")
        with col1:
            st.subheader("🖼️ Image Source")
            image = show_uploaded_file(uploaded_file, caption="Image Originale")
        with col2:
            st.subheader("📝 Résultats OCR")
            if image and st.button("Extraire le Texte", key="extract"):
                with st.spinner("Extraction du texte..."):
                    extracted_text, metadata = perform_ocr(image)
                display_ocr_results(extracted_text, metadata)

if __name__ == "__main__":
    main()
