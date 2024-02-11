# Note: Have mongodb server up and running
import os
import requests
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient


load_dotenv()

uri = os.getenv('uri')
hf_token = os.getenv('hf_token')

client = MongoClient(uri)
db = client.sample_mflix

collections = db.movies

items = collections.find().limit(5)
print(items)

for item in items:
    print(item)



hf_token = hf_token
'''
Sentence Tranformer : https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2
'''
embedding_url = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"

# Todo: Generate Embeddings
def generate_embeddings(text : str) -> list[float]:

    response = requests.post(
        embedding_url,
        headers = {"Authorization": f"Bearer {hf_token}"},
        json = {"input" : text}
    )

    if response.status_code != 200:
        raise ValueError(f"Request failed with status code {response.status_code} : {response.text}")

    return response.json

# Todo: add embeddings to db
for doc in collections.find({'plot':{"$exists": True}}).limit(50): # limit it to first 50
  doc['plot_embedding_hf'] = generate_embeddings(doc['plot'])
  collections.replace_one({'_id': doc['_id']}, doc)

# Todo: Perform vector Search
query = "imaginary characters from outer space at war"

results = collections.aggregate([
    {
        "$vectorSearch" : {
            "queryVector" : generate_embeddings(query),
            "path" : "plot_embedding_hf",
            "numCandidates" : 100,
            "limit" : 4,
            "index" : "PlotSemanticSearch",
        }
    }
]);

for document in results:
    print(f'Movie Name: {document["title"]},\nMovie Plot: {document["plot"]}\n')



