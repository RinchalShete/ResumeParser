from fastapi import FastAPI, File, UploadFile
import os
from app.parser import extract_text_from_pdf, extract_text_from_docx, parse_resume

app = FastAPI()

UPLOAD_DIR = "uploaded_resumes"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload/")
async def upload_resumes(files: list[UploadFile] = File(...)):
    results = []

    for file in files:
        file_path = os.path.join(UPLOAD_DIR, file.filename)

        # Save file locally
        file_bytes = await file.read()
        with open(file_path, "wb") as f:
            f.write(file_bytes)

        # Extract text based on file type
        if file.filename.endswith(".pdf"):
            text = extract_text_from_pdf(file_path)
        elif file.filename.endswith(".docx"):
            text = extract_text_from_docx(file_path)
        else:
            results.append({"filename": file.filename, "error": "Unsupported file format"})
            continue

        # Parse the extracted text
        parsed_data = parse_resume(text)

        results.append({"filename": file.filename, "data": parsed_data})

    # Delete all files in the upload directory after processing
    for f in os.listdir(UPLOAD_DIR):
        file_to_remove = os.path.join(UPLOAD_DIR, f)
        try:
            if os.path.isfile(file_to_remove):
                os.remove(file_to_remove)
        except Exception as e:
            print(f"Error deleting file {file_to_remove}: {e}")

    return {"results": results}
