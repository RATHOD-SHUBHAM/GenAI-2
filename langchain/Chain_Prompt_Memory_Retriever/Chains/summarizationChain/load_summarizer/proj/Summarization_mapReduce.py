import os
from dotenv import load_dotenv

load_dotenv()

from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains.summarize import load_summarize_chain

os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

# Todo. 1. Load the document
file_path = '/Users/shubhamrathod/PycharmProjects/prompt_memory_qa_retriever/Data'
loader = DirectoryLoader(file_path, glob='**/*.pdf', show_progress=True)  # load only pdf from this directory
docs = loader.load()
# print(docs)

# Todo. 2. Chunk the docs
text_chunks = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=300,
    length_function=len,
    is_separator_regex=False
)

documents = text_chunks.split_documents(docs)
# print(documents)

# Todo: 3. Creating Prompt Template
template = """
    Create a concise summary of the given documents, maintaining objectivity and consistency.
    Text: {text}
"""

prompt = PromptTemplate(
    input_variables=['text'], # make sure the input variable name is always text
    template=template
)

# Todo: 4. LLM
llm = ChatOpenAI(temperature = 0, model_name="gpt-3.5-turbo-1106")

# Todo: 5. Summarizer: Map reduce and refine chain usually take time to provide and output
chain = load_summarize_chain(
    llm = llm,
    map_prompt=prompt,
    chain_type='map_reduce'
)

summary = chain.run(documents)
print(summary)