'''
The full sequence from raw data to answer will look like:

Indexing
Load: First we need to load our data. We’ll use DocumentLoaders for this.
Split: Text splitters break large Documents into smaller chunks. This is useful both for indexing data and for passing it in to a model, since large chunks are harder to search over and won’t fit in a model’s finite context window.
Store: We need somewhere to store and index our splits, so that they can later be searched over. This is often done using a VectorStore and Embeddings model.
Retrieval and generation
Retrieve: Given a user input, relevant splits are retrieved from storage using a Retriever.
Generate: A ChatModel / LLM produces an answer using a prompt that includes the question and the retrieved data

'''


import os
from dotenv import load_dotenv

load_dotenv()

os.environ['OPENAI_API_KEY']=os.getenv('OPENAI_API_KEY')


from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAI
from langchain.chains import RetrievalQA

# Todo: 1. Load pdf
file_path='/Users/shubhamrathod/PycharmProjects/prompt_memory_qa_retriever/Data/yoloWorld.pdf'
loader = PyPDFLoader(file_path=file_path)
pages = loader.load()
# print(pages)

# Todo: 2. Chunk Document
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=800,
    length_function=len,
    is_separator_regex=False
)
documents = text_splitter.split_documents(pages)

# Todo: 3.Embeddings
embedding_function = OpenAIEmbeddings()

# Todo: 4. Chroma
persist_directory = 'chroma_db'

if os.path.exists('/Users/shubhamrathod/PycharmProjects/prompt_memory_qa_retriever/chain/retrieverChain/chroma_db'):
    # load from disk
    db = Chroma(persist_directory=persist_directory,
                embedding_function=embedding_function)
else:
    # save to disk
    db = Chroma.from_documents(documents,
                               embedding_function,
                               persist_directory=persist_directory
                               )

# Todo: Similarity Search
query = 'What is Yolo World?'
docs = db.similarity_search(query=query)
print(docs)
# Todo: Similarity search with score
docs = db.similarity_search_with_score(query)
print(docs)
# Todo: Retriever
retriever = db.as_retriever(search_type="mmr")
# retriever = db.as_retriever(search_kwargs={'k': 3})

# Todo: 5. Retrieval QA chain
llm = OpenAI(temperature=0)

qa_chain = RetrievalQA.from_chain_type(
    llm = llm,
    retriever=retriever,
    return_source_documents=True
)

# Todo: 6. Run chain
# result = qa_chain.run(query) # `run` not supported when there is not exactly one output key. Got ['result', 'source_documents'].
result = qa_chain.invoke({'query':'What is Yolo World'})
print(result)
print(result['result'])
