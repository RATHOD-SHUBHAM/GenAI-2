'''
    Chain to run queries against LLMs.
'''

import os
from dotenv import load_dotenv

load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
# OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')


from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI(temperature=0)

template = """
    You are an AI Expert, You answer in detail about the topic asked.
    topic : {topic}
    
    Be specific and answer in bullet points
"""

prompt = PromptTemplate(
    input_variables=["topic"],
    template=template
)

chain = LLMChain(
    llm=llm,
    prompt=prompt,
    output_parser=StrOutputParser(),
    verbose=False
)

result = chain.run('Machine Learning')
print(result)
