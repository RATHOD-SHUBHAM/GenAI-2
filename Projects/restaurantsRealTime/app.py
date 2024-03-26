from entity import Entity
from agent import Agent
from conversational import Conversational

def main(Flag):

    while True:
        query = input('Enter You query: ')

        if query == 'thanks' or query == 'q':
            print('It was a pleasure helping you')
            break

        if Flag == False:

            # First part - User Query(Extract Entity).
            entity_obj = Entity()
            keyword, radius = entity_obj.entity(query=query)
            print(keyword)
            print(radius)

            # Second Part - API Response.
            agent_obj = Agent()
            extracted_info = agent_obj.agent(keyword=keyword, radius=radius)
            print(extracted_info)

            # Third Part: Conversation
            conversational_obj = Conversational()
            conversational_obj.conversational(extracted_info=extracted_info, query=query)

            Flag = True

        elif Flag == True:

            # Third Part: Conversation
            conversational_obj = Conversational()
            conversational_obj.conversational(extracted_info=extracted_info, query=query)

'''

def main_1():
    query = 'Taco place near me'

    # First part - User Query(Extract Entity).
    entity_obj = Entity()
    keyword, radius = entity_obj.entity(query=query)
    print(keyword)
    print(radius)

    # Second Part - API Response.
    agent_obj = Agent()
    extracted_info = agent_obj.agent(keyword=keyword, radius=radius)
    print(extracted_info)

    # Third Part: Conversation
    conversational_obj = Conversational()
    conversational_obj.conversational(extracted_info=extracted_info, query=query)

'''


def clear_memory():
    # Clear the memory
    conversational_obj = Conversational()
    conversational_obj.clear_memory()



if __name__ == '__main__':
    main(Flag = False)
    clear_memory()


