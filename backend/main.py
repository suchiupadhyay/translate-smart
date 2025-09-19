from fastapi import FastAPI, UploadFile, File,Form
from fastapi.responses import FileResponse
import shutil
import os
import uuid
from translator import extract_text_from_pdf, translate_to_hindi, translate_to_gujarati
import fitz
import tempfile


app = FastAPI()

@app.post("/translate-pdf/")
async def translate_pdf(file: UploadFile = File(...),lang: str = Form(...)):
    os.makedirs("temp", exist_ok=True)
    temp_filename = f"temp/{uuid.uuid4()}_{file.filename}"
    
    with open(temp_filename,"wb") as f:
        shutil.copyfileobj(file.file, f) ##shutil copies the file in chunks, not all at once. shutil.copyfileobj() is about streaming, not loading.

    ''' OR we can use simple file.read() operation and the temporaryfile concept we had in frontend
        # Read file content safely
        contents = await file.read()

     # Use tempfile just like in Streamlit frontend
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(contents)
            temp_filename = tmp_file.name  # same as tmp_path in frontend

        '''
    try:
        extracted_text_pages = extract_text_from_pdf(temp_filename)
    except Exception as e:
        return {"error": f"Text extraction failed: {str(e)}"}
    
    translated_pages = []
    for page_text in extracted_text_pages:
        try:
            if lang == "hindi":
                translated = translate_to_hindi(page_text)
            elif lang == "gujarati":
                translated = translate_to_gujarati(page_text)
            else:
                return {"error": f"Unsupported language: {lang}"}
            translated_pages.append(translated)
        except Exception as e:
            translated_pages.append(f"[Translation error]: {str(e)}")

    ## Combine all the pages 
    translated_text = "\n\n--- Page Break ---\n\n".join(translated_pages)

    ## save in txt file and 
    output_file_path = temp_filename.replace(".pdf", f"_{lang}_translated.txt")

    with open(output_file_path, "w", encoding="utf-8") as out_file:
        out_file.write(translated_text)

    return FileResponse(output_file_path, media_type="text/plain", filename=f"translated_{lang}.txt")
    

    ''' if you want to choose download file as pdf then use below code 
            # # CHOOSE FONT BASED ON LANGUAGE
            # if lang == "hindi":
            #     font_path = "fonts/NotoSansDevanagari-Regular.ttf"
            # elif lang == "gujarati":
            #     font_path = "fonts/NotoSansGujarati-Regular.ttf"
            # else:
            #     return {"error": f"No font found for language: {lang}"}


            # # Create PDF
            # output_pdf_path = temp_filename.replace(".pdf", f"_{lang}_translated.pdf")

            # doc = fitz.open()
            # for page_text in translated_pages:
            #     # Create a new blank page
            #     page = doc.new_page()

            #     # Define where to insert text (x, y) starting point
            #     x, y = 50, 50

            #     # Add line by line
            #     for line in page_text.split('\n'):
            #         page.insert_text((x, y), line, fontsize=12,
            #                          fontname="custom",fontfile=font_path)
            #         y += 15  # Move to next line
                
            # # Save the final PDF
            # doc.save(output_pdf_path)
            # doc.close()

            # ## return pdf file to user:
            # return FileResponse(output_pdf_path, media_type="application/pdf", filename=f"translated_{lang}.pdf")
    '''