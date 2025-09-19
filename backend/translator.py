# translate.py
import os
from dotenv import load_dotenv
#import streamlit as st

import google.generativeai as genai
from pdf2image import convert_from_path

load_dotenv()

# Your API Key setup
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if GOOGLE_API_KEY is None:
    raise ValueError("Google API Key is missing. Please set it in the .env file.")

# Configure the Generative AI library with the API key
genai.configure(api_key=GOOGLE_API_KEY)


# Initialize the model
model = genai.GenerativeModel('gemini-1.5-flash')

# Function to extract text from PDF (converted to images)
def extract_text_from_pdf(pdf_file):
    # Convert PDF to images (1 image per page)
    pages = convert_from_path(pdf_file, dpi=300)
    print(f"Total pages: {len(pages)}")
    
    all_responses = []
    
    for i, page in enumerate(pages):
        print(f"Processing page {i+1}...")
        prompt = "Please extract all text from this image."
        response = model.generate_content([prompt, page])
        all_responses.append(response.text)
        print(f"Finished processing page {i+1}.")

    return all_responses

# Function for translating text to Hindi
def translate_to_hindi(english_text):
    prompt_hindi = "Please translate the following text into Hindi:"
    hindi_response = model.generate_content([prompt_hindi, english_text])
    return hindi_response.text

# Function for translating text to Gujarati
def translate_to_gujarati(english_text):
    prompt_gujarati = "Please translate the following text into Gujarati:"
    gujarati_response = model.generate_content([prompt_gujarati, english_text])
    return gujarati_response.text
