import streamlit as st
from PIL import Image
from utils.styles import HEADER_STYLE

def render_header(subtitle=None):
    """Render the dashboard header with logo and optional subtitle"""
    # Inject custom CSS
    st.markdown(HEADER_STYLE, unsafe_allow_html=True)

    # Create two columns for logo and title
    col1, col2 = st.columns([1, 4])

    with col1:
        try:
            logo = Image.open('src/assets/logo.jpg')
            st.image(logo, width=150)
        except:
            st.write("Logo not found")

    with col2:
        st.title("OKR Performance Dashboard")
        if subtitle:
            st.markdown(f'<div class="subtitle">{subtitle}</div>', unsafe_allow_html=True)