'''
API Docs:
    * https://vext.readme.io/reference/http-request-query
'''

import os
from dotenv import load_dotenv

load_dotenv()

Api_key = os.getenv('VEXT_API')


import requests

# Todo: Add Data Source

# url = "https://api.vextapp.com/api/v1/data-source"
#
# payload = { "source": "pdf" }
# headers = {
#     "accept": "application/json",
#     "content-type": "application/json",
#     "Apikey": "Api-Key <API_KEY>"
# }
#
# response = requests.post(url, json=payload, headers=headers)
#
# print(response.text)


# Todo: Request Query

query = "What is yolo world"

endpoint_id = 'G2XV4U86SP'

channel_token = 'testRAG'

url = f"https://payload.vextapp.com/hook/{endpoint_id}/catch/{channel_token}"

payload = { "payload": query }

headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "Apikey": f"Api-Key {Api_key}"
}

response = requests.post(url, json=payload, headers=headers)

print(response.text)