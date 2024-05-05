from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain, ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()
# os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

class Conversational:
    def __init__(self):
        self.memory = ConversationBufferMemory(memory_key="history", return_messages=True)

    def conversational(self, extracted_info, query):
        template = '''
          Your Role:
          - You are a friendly and talkative conversational assistance.

          Your Expertise:
          You remember all the past coversation with the user based on the memory provided below
          Chat History: {history}

          Your expertise is in analyzing and understanding the context provided below,
          Context: {extracted_info}

          The context is a list of dictionary with the following parameter: 'business_status', 'formatted_address', 'name', 'open', 'price_level', 'rating'.

          Use the list below to understand the parameter better:
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

          Keep your response short and clear, and just respond back with the answer and nothing else.
          AI:
        '''

        llm = ChatOpenAI(temperature=0.0)

        prompt = PromptTemplate(
            input_variables=["history", "input"],
            template=template,
            partial_variables={'extracted_info': extracted_info}
        )

        chain = ConversationChain(
            llm=llm,
            prompt=prompt,
            memory=self.memory,
            verbose=False
        )

        query = query
        response = chain.invoke(query)
        print(response['response'])

    def clear_memory(self):
        self.memory.clear()
