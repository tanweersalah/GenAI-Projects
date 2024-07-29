from io import BytesIO
import streamlit as st
import PyPDF2

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    pdf_stream = BytesIO(bytes_data)
    pdf_reader = PyPDF2.PdfReader(pdf_stream)
    resume_text = str()
    
    # Extract text
    for page in pdf_reader.pages:
        resume_text += page.extract_text()
    
    st.success(resume_text)