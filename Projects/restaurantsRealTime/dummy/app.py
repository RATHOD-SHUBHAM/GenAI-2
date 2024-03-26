from googleapi import GoogleAPI
from conversationalagent import  ConversationalAgent

def main(query):
    # google places object
    google_obj = GoogleAPI()
    extracted_info = google_obj.googleapi()

    # conversation object
    query = query
    convo_obj = ConversationalAgent()
    response = convo_obj.conversationalagent(query=query, extracted_info=extracted_info)
    print(response)


if __name__ == '__main__':
    query = 'Give me names of restaurant with rating over 4.5'
    main(query=query)




