# Build the index in pinecone

from langchain_openai import OpenAIEmbeddings
import pinecone
from langchain_community.vectorstores import Pinecone
from langchain_pinecone import PineconeVectorStore
import pandas as pd
from langchain.schema import Document
from tqdm import tqdm
from dotenv import load_dotenv
import os
import time

load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
os.environ['PINECONE_API_KEY'] = os.getenv('PINECONE_API_KEY')
os.environ['environment'] = "gcp-starter"

# Todo: Initialize embeddings
embeddings = OpenAIEmbeddings()

# Todo: Create Documents

# Document skeleton
def doc_skeleton(row):
    return Document(
        page_content=row.description,

        metadata={
            'country': row.country,
            'province': row.province,
            'name': row.title,
            'variety': row.variety,
            'winery': row.winery
        }
    )


# Read CSV file
file_path = '/Users/shubhamrathod/PycharmProjects/CSV_Projects/Wine_Suggestion/data/winemag-data-130k-v2.csv'
df = pd.read_csv(filepath_or_buffer=file_path)
df = df.fillna('')

df = df.sample(600) # get 600 samples

"""
docs = []
for row in tqdm(df.itertuples(index = False)):
    documents = doc_skeleton(row)
    docs.append(documents)
"""
docs = [doc_skeleton(row) for row in tqdm(df.itertuples(index = False))]

# Todo: Build Vectors
'''
I can create form scratch or just add docs to db

1. To add docs

index_name = "wine-db"
vectorstore = PineconeVectorStore(index_name=index_name, embedding=embeddings)
vectorstore.add_texts(docs)

vectorstore.add_texts(["More text!"])
'''
# 2. Create db from scratch
index_name = "wine-db"
start_time = time.perf_counter()
db = PineconeVectorStore.from_documents(docs, embeddings, index_name=index_name)
end_time = time.perf_counter() - start_time

print(f"File uploaded in {end_time} seconds")


