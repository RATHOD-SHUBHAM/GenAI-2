import os
from dotenv import load_dotenv

load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.chains import StuffDocumentsChain
from langchain.chains import ReduceDocumentsChain
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Todo: 1. Load the document
loader = PyPDFLoader('/Users/shubhamrathod/PycharmProjects/prompt_memory_qa_retriever/Data/attention.pdf')
pages = loader.load()

# Todo: 2. Split document
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50,
    length_function=len,
    is_separator_regex=False
)

docs = text_splitter.split_documents(pages)
print(docs)

# Todo 3. Define the model.
llm = ChatOpenAI(temperature=0)

# Todo: 4. Create Prompt Template

template = """
    The following is a set of documents
    {docs}
    Based on this list of docs, give me the main key points
    Helpful Answer:
"""

prompt = PromptTemplate(
    input_variables = ['docs'],
    template=template
)

# Todo: 5. Create chain
chain = LLMChain(
    llm = llm,
    prompt=prompt,
    output_parser=StrOutputParser(),
)

# Todo 6. Stuff the context of document - Summarize
combined_document_chain = StuffDocumentsChain(
    llm_chain=chain,
    document_variable_name='docs',
)

print(combined_document_chain.run(docs))
