import os
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# OpenAi version
import openai
print(openai.__version__)


'''
Prompts
    https://python.langchain.com/docs/modules/model_io/prompts/
    
Types of MessagePromptTemplate
    https://python.langchain.com/docs/modules/model_io/prompts/prompt_templates/msg_prompt_templates

'''


from langchain.prompts import HumanMessagePromptTemplate
from langchain.prompts import ChatPromptTemplate
from langchain.prompts import SystemMessagePromptTemplate

# Prompt
system_template = """
You are a helpful assistant who generate comma separated lists.
A user will only pass a category and you should generate subcategories of that category in a comma separated list.
ONLY return comma separated and nothing more!
"""

human_tempalate = '{Category}'

system_message = SystemMessagePromptTemplate.from_template(
    system_template
)

print(system_message)

human_message = HumanMessagePromptTemplate.from_template(
    human_tempalate
)

print(human_message)

# pass the prompt to the chain
prompt = ChatPromptTemplate.from_messages([
    system_message,
    human_message
])

# pass to the chain

from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI

model = ChatOpenAI()

chain = LLMChain(
    llm=model,
    prompt=prompt,
    verbose = True
)

# chain.run()