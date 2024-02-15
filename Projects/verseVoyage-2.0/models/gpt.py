# Todo: Simple Prompt
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain


class gpt:
    def gpt(self, user_input, openai_api_key ):
        llm = OpenAI(openai_api_key=openai_api_key,
                     temperature=1)

        template = """
            You are an imaginative, humorous, romantic, and intelligent poet. 
            You are comparable to Shakespeare.
            
            Your task is to write poetry about {input}.
    
        """

        # Write a prompt using PromptTemplate
        prompt = PromptTemplate(
            input_variables=["input"],
            template=template,
        )

        # create chain using LLMChain
        chain = LLMChain(llm=llm, prompt=prompt)

        # Run the chain only specifying the input variable.
        user_input = user_input
        response = chain.run(user_input)

        return response
