# Todo: Load the API
import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("OPENAI_API_KEY")

# Todo: Libraries
import streamlit as st

# For streamlit multifile use this
from PyPDF2 import PdfReader

from langchain.text_splitter import RecursiveCharacterTextSplitter

# from langchain_community.vectorstores import Chroma
from langchain_community.vectorstores import FAISS

from langchain.prompts import PromptTemplate

from langchain.chains.question_answering import load_qa_chain

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# Todo: Streamlit Components

# streamlit code for viewing document
st.set_page_config(layout="wide")

# hide hamburger and customize footer
hide_menu = """
<style>

#MainMenu {
    visibility:hidden;
}

footer{
    visibility:visible;
}

footer:after{
    content: 'With 🫶️ from Shubham Shankar.';
    display:block;
    position:relative;
    color:grey;
    padding;5px;
    top:3px;
}
</style>

"""
# Styling ----------------------------------------------------------------------

st.image("icon.jpg", width=85)
st.title("Multi PDF Chat")
st.subheader("Powered by: Google Gemini Pro")
st.markdown(hide_menu, unsafe_allow_html=True)

# Intro ----------------------------------------------------------------------

st.write(
    """

    Hi 👋, I'm **:red[Shubham Shankar]**, and welcome to my **:green[Chat Bot]**! :rocket: This program makes use of **:blue[Large Language Model]** such as **:orange[Gemini Pro]** model, 
    to understand content of the document and reply to **:violet[User Query]** .  ✨

    """
)

st.markdown('---')

st.write(
    """
    ### App Interface!!

    :dog: The web app has an easy-to-use interface. 

    1] **:green[Upload File]**: On the side bar - Upload as many PDF file of your choice using the provided button.

    2] **:violet[Query Docs]**: Ask the Bot a question - Things you want to know from the PDF.

    """
)

st.markdown('---')

st.error(
    """
    Connect with me on [**Github**](https://github.com/RATHOD-SHUBHAM) and [**LinkedIn**](https://www.linkedin.com/in/shubhamshankar/). ✨
    """,
    icon="🧟‍♂️",
)

st.markdown('---')


# Todo: Read and load PDF
def load_pdf(uploaded_file):
    raw_text = ""

    for pdf in uploaded_file:

        pdf_reader = PdfReader(pdf)

        for page in pdf_reader.pages:
            raw_text += page.extract_text()

    return raw_text


# Todo: Get text chunks
def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=10000,
        chunk_overlap=100,
        length_function=len,
        is_separator_regex=False,
    )

    chunks = text_splitter.split_text(text)

    return chunks


# Todo: Convert chunks to vectors
def vector_store(text_chunks):
    # create embedding
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    # load it into Chroma
    db = FAISS.from_texts(text_chunks, embeddings)

    # saving
    db.save_local("faiss_index")


# Todo: Prompt, LLM, Chain
def conversational_chain():
    template = """
        Answer the question as detailed as possible from the provided context, make sure to provide all the details, if the answer is not in
        provided context just say, "answer is not available in the context", don't provide the wrong answer\n\n
        Context:\n {context}?\n
        Question: \n{question}\n

        Answer:
    """

    model = ChatGoogleGenerativeAI(model="gemini-pro",
                                   google_api_key=GOOGLE_API_KEY,
                                   temperature=0.5)

    prompt_template = PromptTemplate(
        input_variables=["context", "question"],
        template=template
    )

    chain = load_qa_chain(llm=model,
                          chain_type="stuff",
                          prompt=prompt_template
                          )

    return chain


# Todo: User Input
def user_input(query):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    new_db = FAISS.load_local("faiss_index", embeddings)

    docs = new_db.similarity_search(query)

    chain = conversational_chain()

    response = chain.invoke(
        {"input_documents": docs, "question": query}
        , return_only_outputs=True)

    # print(response)
    # st.write("Reply: ", response["output_text"])
    return response["output_text"]


def main():

    # Process Document
    with st.sidebar:
        st.title("Menu:")

        pdf_docs = st.file_uploader("Upload your PDF Files: ", accept_multiple_files=True)

        if st.button("Submit"):
            with st.spinner("Processing..."):
                raw_text = load_pdf(pdf_docs)

                text_chunks = get_text_chunks(raw_text)

                vector_store(text_chunks)

                st.success("Processed")

    # User Query

    user_question = st.text_input("Query Docs: ", placeholder = "Type your question here")

    if user_question:
        if st.button('Ask'):
            answer = user_input(user_question)
            st.text_area("The Answer is: ", answer)





if __name__ == "__main__":
    main()
