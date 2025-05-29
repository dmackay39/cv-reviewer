from cv_crew.crew import CvCrew
from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile, Form
from typing import Annotated
import PyPDF2

app = FastAPI()

def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

load_dotenv()

@app.post("/uploadfile/")
async def create_upload_file(job_desc: Annotated[str, Form()], cv_file: Annotated[UploadFile, File()]):
    cv_text = extract_text_from_pdf(cv_file.file)
    inputs = {
        "job_description": job_desc,
        "cv_text": cv_text
    }

    try:
        result = CvCrew().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")
    
    return result