import os
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain.prompts.prompt import PromptTemplate
from langchain.chains import RetrievalQA

from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
os.environ['PINECONE_API_KEY'] = os.getenv('PINECONE_API_KEY')
# index name for pine cone
os.environ['environment'] = "aws"

# Todo: Load the document
HOME = os.getcwd()
file_path = f'{HOME}/docs'
loader = DirectoryLoader(file_path, show_progress=True)
pages = loader.load()

# Todo: Chunk the data
text_splitter = RecursiveCharacterTextSplitter(
    # Set a really small chunk size, just to show.
    chunk_size=10000,
    chunk_overlap=3000,
    length_function=len,
    is_separator_regex=False,
)

docs = text_splitter.split_documents(pages)

# Todo: Create Embeddigns
embeddings = OpenAIEmbeddings()

# Todo: Store in DB
index_name = "pcbdefect"
index = PineconeVectorStore.from_documents(docs, embeddings, index_name=index_name)

# Todo: Create a retriever
retriever = index.as_retriever(search_type="mmr")

# Todo: Load the Chain
llm = ChatOpenAI(temperature=0)

template = """
  You are expert in identifying, understanding and explaining any defects that occur on a PCB board.
  Given the context and question below, your task is to answer every question that the user ask in great detail and in a well structured format , Use bullet points if required while explaining.
  
  Context: {context}
  
  Question: {question}
"""

prompt = PromptTemplate(
    template=template,
    input_variables=["context", "question"]
)

chain_type_kwargs = {"prompt": prompt}


def chatbot(query):
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs=chain_type_kwargs,
        return_source_documents=True
    )

    result = qa_chain.invoke({'query': query})

    return result
