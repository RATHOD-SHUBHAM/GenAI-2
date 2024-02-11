# https://python.langchain.com/docs/integrations/vectorstores/mongodb_atlas
import os

from pymongo import MongoClient
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import MongoDBAtlasVectorSearch
from langchain_openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv('MONGO_URI')
openai_api = os.getenv('openai_api')

# Todo: Access Database

client = MongoClient(MONGO_URI)
dbName = 'langchain_demo'
collectionName = 'collection_of_text_blobs'
collection = client[dbName][collectionName]

# 1. Get access to embeddings and vector store
embeddings = OpenAIEmbeddings(openai_api_key = openai_api)
vector_search = MongoDBAtlasVectorSearch(collection, embeddings)

llm = ChatOpenAI()

retriever = vector_search.as_retriever()

def query_data(query):
    docs = vector_search.similarity_search(query, k=1)

    as_output = docs[0].page_content # Similar docs from vector

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
    )

    retriever_op = qa(query) # op from LLm

    return as_output , retriever_op


if __name__ == '__main__':
    user_input = input("Question: ")
    vector_op , llm_op = query_data(user_input)


