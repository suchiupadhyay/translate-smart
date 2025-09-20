# 🌍 Translate Smart

**Translate Smart** is a full-stack translation application built with:

- 🖼️ [Streamlit](https://streamlit.io/) – for the frontend UI
- ⚙️ [FastAPI](https://translate-smart.onrender.com/) – for the backend API
- 🌐 Deployed using [Streamlit Cloud](https://streamlit.io/cloud) and [Render](https://render.com/)

---


## 📂 Project Structure
```bash

translate-smart/

├── app.py                  ✅ Streamlit entry point
├── requirements.txt        ✅ For Streamlit Cloud
├── backend/
│   ├── main.py             ✅ FastAPI backend
│   ├── translator.py
│   └── requirements.txt
    |__ runtime.txt         ✅ python version defined for render to use

├── render.yaml             ✅ Used by Render to deploy backend
```

    
### Architecture Diagram
```bash

   ┌────────────────────────────┐
   │  Streamlit Frontend (UI)  │     ← On Streamlit Cloud
   │  https://yourname.streamlit.app
   └────────────┬──────────────┘
                │
      HTTP POST /translate
                │
   ┌────────────▼──────────────┐
   │ FastAPI Backend (API)     │     ← On Render
   │ https://translate-smart.onrender.com
   └───────────────────────────┘
```

---

## 🚀 Getting Started

### 1. 🔧 Install Prerequisites

Ensure you have Python 3.9+ installed.  
We recommend using a virtual environment.


```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. 🧪 Run Locally

Start FastAPI Backend

    cd backend
    uvicorn main:app --reload --host 0.0.0.0 --port 8000


Start Streamlit Frontend
    In a new terminal:
    streamlit run app.py


### 3. 🔁 Project Workflow

    - User upload pdf file in Streamlit

    - Streamlit sends a request to FastAPI (/translate)

    - FastAPI uses logic in translator.py to process translation

    - Response is shown in the Streamlit UI


### 4. ☁️ Deployment

    ✅ Deploy FastAPI on Render

    ✅ Deploy Streamlit on Streamlit Cloud


### 5. 📜 Logging (Debugging)

To help with debugging, logs are captured in:

    app.log – logs from frontend (Streamlit)

    fastapi.log – logs from backend (FastAPI) ## pending

    You can also view logs inside the Streamlit UI via an expander section ## verified but not require in UI


and finally, frontend is live : https://translate-smart-ui.st.app/
