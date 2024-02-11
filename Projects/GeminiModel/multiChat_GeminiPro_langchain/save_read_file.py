import streamlit as st
import os
from langchain_community.document_loaders import PyPDFLoader
from PyPDF2 import PdfReader


def save_file(files):
    for file in files:
        with open(os.path.join("tempFile", file.name), "wb") as f:
            f.write(file.getbuffer())

    return st.success("Saved File to tempFile")

# Todo: Read and load PDF
def load_pdf(uploaded_file):
    raw_text = ""

    for pdf in uploaded_file:

        pdf_reader = PdfReader(pdf)

        for page in pdf_reader.pages:
            raw_text += page.extract_text()

    return raw_text


uploaded_files = st.file_uploader("Upload documents", accept_multiple_files=True, type=["txt", "pdf"])

if uploaded_files:
    if st.button('RUN'):

        textify_output = save_file(uploaded_files)

        raw_text = load_pdf(uploaded_files)
        print(raw_text)