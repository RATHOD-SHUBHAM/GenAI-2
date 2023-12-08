import os
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# OpenAi version
import openai
print(openai.__version__)

'''
Memory Types:
    https://python.langchain.com/docs/modules/memory/types/
    

Conversation Buffer:
    https://python.langchain.com/docs/modules/memory/types/buffer
    
    This memory allows for storing messages and then extracts the messages in a variable.


    
Customizing Conversational Memory:
    https://python.langchain.com/docs/modules/memory/conversational_customization
    
    This notebook walks through a few ways to customize conversational memory.
'''

# Using in a chain

from langchain.chains import ConversationChain
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferMemory

llm = OpenAI(temperature=0)

## AI Prefix
### Here it is by default set to "AI" , setting verbose=True so we can see the prompt
conversation = ConversationChain(
    llm=llm,
    verbose=True, # we can see different prompt that we pass to LLM
    memory=ConversationBufferMemory()
)

### Prediction
# conversation.predict(input="Hi there!")
