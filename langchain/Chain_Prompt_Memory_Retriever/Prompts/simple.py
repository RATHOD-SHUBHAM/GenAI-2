import os
from dotenv import load_dotenv
from langchain.prompts.prompt import PromptTemplate
from langchain_openai import OpenAI
from langchain.chains import LLMChain

load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

template = '''
Answer the question based on the context below. If the question cannot be answered using the information provided answer
with "I don't know".

Context: Large Language Models (LLMs) are the latest models used in NLP.
Their superior performance over smaller models has made them incredibly
useful for developers building NLP enabled applications. These models
can be accessed via Hugging Face's `transformers` library, via OpenAI
using the `openai` library, and via Cohere using the `cohere` library.

Question: {query}

Answer:
'''

prompt = PromptTemplate(
    input_variables=["query"],
    template=template
)

# print(prompt.format(query = "Which libraries and model providers offer LLMs?"))

llm = OpenAI(temperature=1)

chain = LLMChain(
    llm=llm,
    prompt=prompt,
    verbose=False
)

query = "Which libraries and model providers offer LLMs?"
response = chain.run(query)
print(response)
