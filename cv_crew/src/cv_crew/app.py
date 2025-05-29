import streamlit as st
from crew import CvCrew
from dotenv import load_dotenv
import PyPDF2

def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

load_dotenv()

st.title("CV & Cover Letter Tool")

st.write("Upload your CV (PDF) and provide a job description to generate feedback and a tailored cover letter.")

uploaded_cv = st.file_uploader("Upload your CV (PDF)", type=["pdf"])
job_description = st.text_area("Paste the job description here")

if st.button("Run Crew") and uploaded_cv and job_description:
    cv_text = extract_text_from_pdf(uploaded_cv)
    inputs = {
        "job_description": job_description,
        "cv_text": cv_text,
    }

    with st.spinner("Running the crew..."):
        try:
            result = CvCrew().crew().kickoff(inputs=inputs)
            st.success("Crew run complete!")

            # Layout: two columns for CV Review and Cover Letter
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("CV Review")
                cv_review = result.get("cv_review_task")
                st.markdown(cv_review if cv_review else "No CV review found.")

            with col2:
                st.subheader("Cover Letter")
                cover_letter = result.get("cover_letter_task")
                st.markdown(cover_letter if cover_letter else "No cover letter found.")

        except Exception as e:
            st.error(f"An error occurred: {e}")