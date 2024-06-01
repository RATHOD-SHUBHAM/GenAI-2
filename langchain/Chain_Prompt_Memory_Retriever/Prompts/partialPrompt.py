from datetime import datetime
import os
from dotenv import load_dotenv
from langchain.prompts.prompt import PromptTemplate
from langchain_openai import OpenAI
from langchain.chains import LLMChain

load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')


"""
The use case for this is when you have a variable you know that you always want to fetch in a common way. 
A prime example of this is with date or time. 
Imagine you have a prompt which you always want to have the current date. 
You can’t hard code it in the prompt, and passing it along with the other input variables is a bit annoying. 
In this case, it’s very handy to be able to partial the prompt with a function that always returns the current date.
"""


def _get_datetime():
    now = datetime.now()
    return now.strftime("%m/%d/%Y, %H:%M:%S")

template = '''
Tell me a {adjective} about this {date}
'''

prompt = PromptTemplate(
    input_variables=["adjective"],
    template=template,
    partial_variables = {'date' : _get_datetime}
)

# print(prompt.format(query = "Which libraries and model providers offer LLMs?"))

llm = OpenAI(temperature=1)

chain = LLMChain(
    llm=llm,
    prompt=prompt,
    verbose=False
)

adjective = "Funny"
response = chain.run(adjective)
print(response)


