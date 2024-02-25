from langchain.chains import LLMChain, SimpleSequentialChain, SequentialChain
from langchain.prompts import PromptTemplate
from langchain.prompts import load_prompt
from langchain_openai import OpenAI
import os

class Backend_Blogger:

    def backend_blogger(self, topic, openai_api_key):
        llm = OpenAI(temperature=1.0, openai_api_key=openai_api_key)
        # Todo: load title prompt
        title_file_name = 'prompts/title_prompt.json'
        title_file_path = os.path.abspath(title_file_name)
        title_prompt = load_prompt(title_file_path)

        title_chain = LLMChain(
            llm=llm,
            prompt=title_prompt,
            output_key='title'
        )

        # Todo: load script prompt
        script_file_name = 'prompts/script_prompt.json'
        script_file_path = os.path.abspath(script_file_name)
        script_prompt = load_prompt(script_file_path)

        script_chain = LLMChain(
            llm=llm,
            prompt=script_prompt,
            output_key='script'
        )

        # Todo: load summarizer prompt
        summary_file_name = 'prompts/summary_prompt.json'
        summary_file_path = os.path.abspath(summary_file_name)
        summary_prompt = load_prompt(summary_file_path)

        summary_chain = LLMChain(
            llm=llm,
            prompt=summary_prompt,
            output_key='summary'
        )

        # Todo: Sequential Chain
        # With simple sequential chain -> we will only get output from last chain
        chain = SequentialChain(
            chains=[title_chain, script_chain, summary_chain],
            input_variables=['topic'],
            output_variables=['title', 'script', 'summary']
        )

        response = chain.invoke(input=topic)

        return response