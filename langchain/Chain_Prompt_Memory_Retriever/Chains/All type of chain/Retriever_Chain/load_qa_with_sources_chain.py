import os
from dotenv import load_dotenv

load_dotenv()

# os.environ['OPENAI_API_KEY']=os.getenv('OPENAI_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')


from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chat_models import ChatOpenAI
from langchain.chains.qa_with_sources import load_qa_with_sources_chain


llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY,
                 temperature=0)


# 1. Load the data.
loader = PyPDFLoader("../../Data/yoloWorld.pdf")
pages = loader.load()

# 2. Chunk the document.
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=300,
    length_function=len,
    is_separator_regex=False
)

documents = text_splitter.split_documents(pages)
# print(documents)

# 3. Create Chain
chain = load_qa_with_sources_chain(
    llm=llm,
    chain_type='map_reduce'
)

# 4. Run the chain
query = "Explain yolo world"

response = chain.invoke({'input_documents': documents, 'question': query})
print(response)