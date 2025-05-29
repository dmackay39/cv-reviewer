from cv_crew.crew import CvCrew
from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException
from typing import Annotated
import PyPDF2

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Only allow React dev server
    allow_credentials=True,
    allow_methods=["POST"],  # Only allow POST requests
    allow_headers=["content-type"],  # Only allow multipart form data and common headers
)

def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

load_dotenv()

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

@app.post("/uploadfile/")
async def create_upload_file(job_desc: Annotated[str, Form()], cv_file: Annotated[UploadFile, File()]):
    if cv_file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")
    # Limit file size
    contents = await cv_file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large.")
    try:
        cv_text = extract_text_from_pdf(cv_file.file)
    except Exception:
        raise HTTPException(status_code=400, detail="Failed to read PDF file.")

    inputs = {
        "job_description": job_desc,
        "cv_text": cv_text
    }

    try:
        result = CvCrew().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while running the crew.")
    
    return result