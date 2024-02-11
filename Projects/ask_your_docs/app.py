import os

import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA

# Page title
st.set_page_config(page_title='🦜🔗 Talk To Doc')
st.title('🦜🔗 Talk To Doc')


def save_uploadedfile(uploadedfile):
    os.makedirs("inputDir", exist_ok=True)
    with open(os.path.join("inputDir", uploadedfile.name), "wb") as f:
        f.write(uploadedfile.getbuffer())

    filename = uploadedfile.name
    return st.success(f"Saved File:{filename} to inputDir")


def generate_response(uploaded_file_name, openai_api_key, query):
    if uploaded_file is not None:
        file_path = 'inputDir/'+ uploaded_file_name
        loader = PyPDFLoader(file_path)
        pages = loader.load()

        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=800,
            length_function=len,
            is_separator_regex=False,
        )

        texts = text_splitter.split_documents(pages)

        # Select embeddings
        embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

        # Create vector store
        db = Chroma.from_documents(texts, embeddings)

        # Create Retriever
        retriever = db.as_retriever()

        # Create QA Chain
        qa = RetrievalQA.from_chain_type(
            llm=ChatOpenAI(openai_api_key=openai_api_key),
            chain_type='stuff',
            retriever=retriever
        )

        return qa.run(query)


# File upload
uploaded_file = st.file_uploader('Upload an article', type='pdf')
if uploaded_file:
    save_uploadedfile(uploaded_file)

# Query text
query = st.text_input('Enter your question:', placeholder = 'Please provide a short summary.', disabled=not uploaded_file)

# Form input and query
result = []
with st.form('myform', clear_on_submit=True):
    openai_api_key = st.text_input('OpenAI API Key', type = 'password', disabled=not (uploaded_file and query))
    submitted = st.form_submit_button('Submit', disabled=not (uploaded_file and query))

    if submitted and openai_api_key.startswith('sk-'):
        with st.spinner('Processing'):
            response = generate_response(uploaded_file.name, openai_api_key, query)
            result.append(response)
            del openai_api_key


if len(result):
    st.info(result)