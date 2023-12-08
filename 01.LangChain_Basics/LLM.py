import os
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# OpenAi version
import openai
print(openai.__version__)

# Langchain LLM

'''
Model I/O
https://python.langchain.com/docs/modules/model_io/

LLM:
    LLMs in LangChain refer to pure text completion models

ChatModel:
    Chat models are often backed by LLMs but tuned specifically for having conversations.

'''

# Chat model
from langchain.chat_models import ChatOpenAI

chat = ChatOpenAI()

# chat.predict('Hi How are You')

# LLM
from langchain.llms import OpenAI

llm = OpenAI()

# llm.predict('Hi how are you')


