import os
from dotenv import load_dotenv

load_dotenv()

os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAI
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain.chains import ConversationalRetrievalChain

# Todo: 1. Load all the file from directory
loader = DirectoryLoader('/Users/shubhamrathod/PycharmProjects/prompt_memory_qa_retriever/Data',
                         glob='**/*.pdf',
                         show_progress=True)
docs = loader.load()
# print(docs)

# Todo: 2. Chunk Document
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=800,
    length_function=len,
    is_separator_regex=False
)
documents = text_splitter.split_documents(docs)

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
# retriever = db.as_retriever(search_type="mmr")
# retriever = db.as_retriever(search_kwargs={'k': 3})

# Todo: Multi Query retriver
'''
The MultiQueryRetriever automates the process of prompt tuning by using an LLM to generate multiple queries from different perspectives for a given user input query
'''
retriever = MultiQueryRetriever.from_llm(
    retriever = db.as_retriever(),
    llm= OpenAI(temperature=0)
)

# Todo: 5. Conversation Retrieval QA chain
llm = OpenAI(temperature=0)

convo_qa_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    return_source_documents=True
)

# Todo: 6. Run chain
chat_history = []

while True:
    query = input('Enter you text: ')
    if query == 'exit' or query == 'quit' or query == 'q':
        break
    elif query =='':
        print('Empty Query')
        continue
    else:
        result = convo_qa_chain.invoke({
            'question' : query,
            'chat_history' : chat_history
        })

        print(result)
        print('History: ',result['chat_history'])
        print('Answer: ',result['answer'])
        # Todo: We got to manually append chat history
        chat_history.append((query, result['answer']))

