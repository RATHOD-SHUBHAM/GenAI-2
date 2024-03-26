from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv
load_dotenv()

os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

class ConversationalAgent:
    def conversationalagent(self, query, extracted_info):
        llm = ChatOpenAI(temperature=0)

        template = '''
            Your Role:
            - You are a friendly and talkative conversational assistance.
    
            Your Expertise:
            - Your expertise is in analyzing and understanding the context provided below,
            Context: {extracted_info}
    
            Use the list below to understand the context better:
            List = [
              'business_status' : Indicates whether the business is currently operational or not.
              'formatted_address' : The place's address.
              'name' : The name of the place.
              'open' : Indicates whether the place is open if it is true, otherwise, it is closed.
              'price_level' : Indicates how pricey the location is.
              'rating' : Refers to the overall rating of the place out of 5. 
            ] 
    
            Your Task:
            - Use the above context and key to help you understand and think of an answer in a step-by-step approach, then respond to the user's question below.
            User question: {input}
    
            Highlight all the findings in a bulleted point, and present your analysis in clear, well-structured markdown format.
        '''

        prompt = PromptTemplate(
            input_variables=["input"],
            template=template,
            partial_variables={'extracted_info': extracted_info}
        )

        chain = LLMChain(
            llm=llm,
            prompt=prompt,
            verbose=False
        )

        query = query
        response = chain.run(query)
        return response