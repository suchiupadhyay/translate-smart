# app.py

import io
import streamlit as st
import tempfile
import requests

# fastapi backend URL
BACKEND_URL = "https://translate-smart.onrender.com"

# Streamlit UI setup
st.title("Scanned PDF Translator")
st.markdown("Upload a scanned PDF, extract text, and translate it to Hindi or Gujarati.")

# File uploader widget
uploaded_pdf = st.file_uploader("Upload PDF", type="pdf")

# Handling the uploaded PDF
if uploaded_pdf is not None:
    target_language = st.selectbox("Select Target Language", ["Hindi", "Gujarati"])

    if st.button(f"Translate to {target_language}"):
        with st.spinner("Extracting text from PDF..."):
            ## Save uploaded file to temp
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(uploaded_pdf.read())
                tmp_path = tmp_file.name

            try:

                with open(tmp_path, "rb") as f:
                    files = {"file": (uploaded_pdf.name, f, "application/pdf")}
                    data = {"lang": target_language.lower()}
                    response = requests.post(f"{BACKEND_URL}/translate-pdf", files=files, data=data,timeout=30)    
        
                if response.status_code == 200:
                    st.success("✅ Translation complete!")
                    st.download_button(
                        label=f"⬇️ Download Translated Text file ({target_language})",
                        data=response.content,
                        file_name=f"translated_{target_language}.txt",
                        mime="text/plain"
                )
                else:
                    st.error(f"❌ Translation failed: {response.status_code}\n{response.text}")

            except Exception as e:
                st.error(f"⚠️ Error contacting backend: {e}")


        