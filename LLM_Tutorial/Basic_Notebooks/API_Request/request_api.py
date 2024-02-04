# https://python.langchain.com/docs/integrations/toolkits/json

# Todo: Load libraries
import os
from dotenv import load_dotenv

# Todo: Getting the access key
load_dotenv()  # take environment variables from .env.
access_key = os.getenv('access_key')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

import requests
import json

# The API endpoint
url = "https://timeapi.io/api/Time/current/zone?timeZone=Japan"

# A GET request to the API
response = requests.get(url)

# Print the response
response_json = response.json()
print(response_json)

with open('data.json', 'w') as f:
    json.dump(response_json, f)

from langchain.chat_models import ChatOpenAI
from langchain.agents import create_json_agent
from langchain.agents.agent_toolkits import JsonToolkit
from langchain.tools.json.tool import  JsonSpec

file="data.json"
with open(file,"r") as f1:
    data=json.load(f1)
    f1.close()

spec=JsonSpec(dict_=data,max_value_length=4000)
toolkit=JsonToolkit(spec=spec)
agent=create_json_agent(llm=ChatOpenAI(temperature=0,model="gpt-4"),toolkit=toolkit,max_iterations=1000,verbose=True)

print(agent.run("what is the time"))
