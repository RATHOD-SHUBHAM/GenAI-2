import os
from dotenv import load_dotenv
from langchain.prompts.prompt import PromptTemplate
from langchain_openai import OpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain

load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

memory = ConversationBufferMemory(memory_key="history", return_messages=True)
# memory = ConversationBufferMemory()
# memory = ConversationBufferMemory(ai_prefix="AI Assistant")
# memory = ConversationBufferMemory(human_prefix="Friend")

# Todo: Npte : ConversationChain only allows to use 'history', and 'input' as input variables for the PromptTemplate, nothing more, nothing less.
template = '''
You are a friendly conversational bot.
Answer the question based on the context below. If the question cannot be answered using the information provided answer
with "I don't know".

Context: Large Language Models (LLMs) are the latest models used in NLP.
Their superior performance over smaller models has made them incredibly
useful for developers building NLP enabled applications. These models
can be accessed via Hugging Face's `transformers` library, via OpenAI
using the `openai` library, and via Cohere using the `cohere` library.

Chat History: {history}

Human: {input}

AI:
'''

prompt = PromptTemplate(
    input_variables=["history","input"],
    template=template
)

# print(prompt.format(query = "Which libraries and model providers offer LLMs?"))

llm = OpenAI(temperature=1)

chain = LLMChain(
    llm=llm,
    prompt=prompt,
    memory=memory,
    verbose=True
)

# query = "Which libraries and model providers offer LLMs?"
# response = chain.run(query)
# print(response)

while True:
    query = input("Enter input here: ")
    if query == 'q' or query == "quit" or query == 'exit':
        break
    if query == '':
        print("Input query")
        continue
    else:
        response = chain.run(query)
        print(response)