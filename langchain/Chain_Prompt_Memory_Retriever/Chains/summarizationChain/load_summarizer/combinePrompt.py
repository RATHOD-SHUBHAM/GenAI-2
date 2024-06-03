import os
from dotenv import load_dotenv
load_dotenv()

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain.prompts import PromptTemplate

os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

# Todo 1. Load the document
file_path = '/Users/shubhamrathod/PycharmProjects/prompt_memory_qa_retriever/Data/attention.pdf'
pdf_loader = PyPDFLoader(file_path=file_path)
pages = pdf_loader.load()

# Todo: 2. Chunk the document
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=20,
    length_function=len,
    is_separator_regex=False,
)
docs = text_splitter.split_documents(pages)

# Todo: 3. Create Combined Prompt
map_template = """
    The following is a set of documents
    
    {docs}
    
    Based on this list of docs, please identify the main themes
    Helpful Answer:
"""

combine_template = """
    The following is a set of summaries:
    
    {docs}
    
    Take these and distill it into a final, consolidated list of the main themes.
    Return that list as a comma separated list.
    Helpful Answer:
"""


map_prompt = PromptTemplate.from_template(map_template)
combine_prompt = PromptTemplate.from_template(combine_template)

llm = ChatOpenAI(temperature = 0, model_name="gpt-3.5-turbo-1106")

chain = load_summarize_chain(
    llm=llm,
    chain_type='map_reduce',
    map_prompt=map_prompt,
    combine_prompt=combine_prompt,
    verbose=True
)

print(chain.run(docs))