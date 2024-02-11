# https://python.langchain.com/docs/integrations/vectorstores/mongodb_atlas
import os

from pymongo import MongoClient
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import MongoDBAtlasVectorSearch
from langchain_openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader

load_dotenv()

MONGO_URI = os.getenv('MONGO_URI')
openai_api = os.getenv('openai_api')

# Todo: Access Database

client = MongoClient(MONGO_URI)
dbName = 'langchain_demo'
collectionName = 'collection_of_text_blobs'
collection = client[dbName][collectionName]

# Todo: Insert data to DB

# 1. Load the PDF
loader = DirectoryLoader('./sample_files', glob="./*.txt", show_progress=True)
docs = loader.load()

# 2. Create Embeddings
from langchain_openai import OpenAIEmbeddings

# insert the documents in MongoDB Atlas with their embedding
vector_search = MongoDBAtlasVectorSearch.from_documents(
    documents=docs,
    embedding=OpenAIEmbeddings(openai_api_key = openai_api),
    collection=collection
)

# 3. Create Index in MongoDB.




