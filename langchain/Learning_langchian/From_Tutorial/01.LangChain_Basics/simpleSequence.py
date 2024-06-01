import os
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# OpenAi version
import openai
print(openai.__version__)


'''
Prompt pipelining
    https://python.langchain.com/docs/modules/model_io/prompts/prompt_templates/prompts_pipelining

Sequential
    https://python.langchain.com/docs/modules/chains/foundational/sequential_chains
'''

from langchain.prompts import PromptTemplate

synopsis_prompt = PromptTemplate.from_template(
        """
            You are a playwright. Given the title of play, it is your job to write a synopsis for that title.
        
            Title: {title}
            Playwright: This is a synopsis for the above play:
        """
    )

review_prompt = PromptTemplate.from_template(
    """
        You are a play critic from the New York Times. Given the synopsis of play, it is your job to write a review for that play.
    
        Play Synopsis:
        {synopsis}
        Review from a New York Times play critic of the above play:
    """
    )

from langchain.chains import LLMChain
from langchain.llms import OpenAI

# This is an LLMChain to write a synopsis given a title of a play.
llm = OpenAI(temperature=0.7)
synopsis_chain = LLMChain(llm=llm, prompt=synopsis_prompt)

# This is an LLMChain to write a review of a play given a synopsis.
llm = OpenAI(temperature=0.7)
review_chain = LLMChain(llm=llm, prompt=review_prompt)

# This is the overall chain where we run these two chains in sequence.
from langchain.chains import SimpleSequentialChain

overall_chain = SimpleSequentialChain(
    chains=[synopsis_chain, review_chain], verbose=True
)

# review = overall_chain.run("Tragedy at sunset on the beach")