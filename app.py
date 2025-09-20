# app.py

import io
import streamlit as st
import tempfile
import requests

## adding Logging
import logging
import io

# In-memory buffer for UI display
log_buffer = io.StringIO()
memory_handler = logging.StreamHandler(log_buffer)

# File handler for persistent logs
file_handler = logging.FileHandler("app.log")

# Console handler for Codespaces terminal
console_handler = logging.StreamHandler()

# Clear any existing handlers (avoid duplicates if Streamlit reruns)
root_logger = logging.getLogger()
if root_logger.hasHandlers():
    root_logger.handlers.clear()

# Configure all handlers
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        memory_handler,    #  for UI
        file_handler,      #  for file
        console_handler    #  for terminal
    ]
)

# Log something
logging.info("Streamlit app started")


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
        st.write("Starting translation request..written by me....")
        with st.spinner("Extracting text from PDF..."):
            ## Save uploaded file to temp
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(uploaded_pdf.read())
                tmp_path = tmp_file.name
                
            try:

                with open(tmp_path, "rb") as f:
                    files = {"file": (uploaded_pdf.name, f, "application/pdf")}
                    data = {"lang": target_language.lower()}
                    response = requests.post(f"{BACKEND_URL}/translate-pdf", files=files, data=data)  # specified timeout=30 also but then get timeout error during processing from streamlit UI to fastapi on render so finally remove timeout attribute.  
                    logging.info(f"📤 Sending request to FastAPI: {BACKEND_URL} | Body: {response.text}")
                    
                st.write(f"Response status code: {response.status_code}")
                    
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
            
            except requests.exceptions.Timeout:
                st.error("Request timed out. Please try again later.")
            except Exception as e:
                logging.exception("❌ Exception while calling FastAPI")
                st.error(f"⚠️ Error contacting backend: {e}")


        