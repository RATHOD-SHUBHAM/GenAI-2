# Todo: Simple Prompt
from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain


class gemini:
    def gemini(self, user_input, google_api_key):
        llm = GoogleGenerativeAI(model="gemini-pro",
                                 google_api_key=google_api_key,
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