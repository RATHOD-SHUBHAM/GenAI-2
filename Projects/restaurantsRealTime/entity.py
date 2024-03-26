from langchain.chains import LLMChain
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

class Entity:

    def entity(self, query):

        entity_template = """
          You are an Intelligent AI assistant who specializes in extracting entities from user questions about restaurants.
        
          The two possible entities are listed below, along with a brief summary of the actions that will be carried out.
        
          Keyword: If a user requests or expresses a preference for a specific sort of cuisine or restaurant (for example, Tacos, Italian, Chinese, Indian food, Mexican restaurant), return back the sort of cuisine.
          Distance: If the user indicates distance or range of distance, extract this information exclusively as "numbers" (for example, "5 miles", "within 2 miles").
          None: If no match is discovered.  
        
        
          Your Task:
          Based on the user query given below,
          Users Query: {query}
        
          First, analyze the users query, and then precisely identify and extract the entities.
        
          If the distance is in miles, convert it to meters by multiplying by 1609.
        
          If the user asks like near me or around me or if the intent is None, use the default value: keyword = restaurant, radius = 4828 meters.  
        
          Respond with only this and nothing else:
            keyword = Keyword
            radius = Distance
        """

        prompt_template = PromptTemplate(
            input_variables=["query"],
            template=entity_template
        )

        model = OpenAI(temperature=0)

        entity_chain = LLMChain(
            llm=model,
            prompt=prompt_template,
            verbose=False
        )

        query = query

        response = entity_chain.invoke(query)
        empty, keyword, radius = response['text'].split('\n')
        # print(keyword, radius)
        keyword = keyword.split(' ')[-1]
        radius = int(radius.split(' ')[-2])

        return keyword, radius