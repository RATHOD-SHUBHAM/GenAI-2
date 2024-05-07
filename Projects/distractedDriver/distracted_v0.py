import os

# Load env
os.environ["OPENAI_API_TYPE"] = "azure_ad"
os.environ["OPENAI_API_VERSION"] = "2024-02-15-preview"
os.environ["AZURE_OPENAI_ENDPOINT"] = "https://mobility-sage-openai-services.openai.azure.com/"
os.environ["AZURE_OPENAI_API_KEY"] = '9bbf92a17be24c66881eaa5a1c6aa77d'

# Todo: Import Libraries
from langchain.prompts.few_shot import FewShotPromptTemplate
from langchain.prompts.prompt import PromptTemplate
from langchain.chains import LLMChain
from langchain_openai import AzureChatOpenAI

llm = AzureChatOpenAI(
    temperature=0,
    azure_deployment="gpt-35-turbo",
)

# Todo: Few Shot Prompt for user query
examples = [
    {
        "query": "Howdy",
        "answer": "Greeting:Normal"
    },
    {
        "query": "Get me home real quick",
        "answer": "Home:Urgent"
    },
    {
        "query": "I am craving something yummy",
        "answer": "Hungry:Normal"
    },
    {
        "query": "My stomach is making some noise due to hunger",
        "answer": "Hungry:Urgent"
    },
    {
        "query": "Lets feed on some Tacos and burritos",
        "answer": "Mexican Restaurant:Normal"
    },
    {
        "query": "A biryani real quick will help me feel a lot better",
        "answer": "Indian Restaurant:Urgent"
    },
    {
        "query": "Lets sit down and relax while grabbing something hot to drink",
        "answer": "Coffee Shop:Normal"
    },
    {
        "query": "Lets go pick up some medicine",
        "answer": "Hospital:Normal"
    },
    {
        "query": "I feel sick",
        "answer": "Hospital:Urgent"
    },
    {
        "query": "My heart is pounding",
        "answer": "Hospital:Urgent"
    },
    {
        "query": "I have got a lot of work that needs to be completed today",
        "answer": "Office:Normal"
    },
    {
        "query": "My day looks pretty tight at work, lets quickly head there",
        "answer": "Office:Urgent"
    },
    {
        "query": "You need to fill up.",
        "answer": "Charging Station:Normal"
    },
    {
        "query": "Stop right here",
        "answer": "Parking:Normal"
    },
    {
        "query": "Am ready to leave",
        "answer": "Summon Vehicle:Normal"
    },
    {
        "query": "Hurry up",
        "answer": "Increase:Urgent"
    },
    {
        "query": "you need to slow down",
        "answer": "Decrease:Normal"
    },
    {
        "query": "Lets enter an infinite loop",
        "answer": "Loop:Normal"
    },
    {
        "query": "Lets get going",
        "answer": "Location:Normal"
    },
    {
        "query": "Come pick me immediately",
        "answer": "Summon Vehicle:Urgent"
    }
]


# Todo: Function Call for chaining the prompt
def LLM_Call(query):
    example_template = """
        Input: {query}
        AI: {answer}
    """

    # create a prompt example from above template
    example_prompt = PromptTemplate(
        input_variables=["query", "answer"],
        template=example_template
    )

    # Todo: Feed examples and formatter to FewShotPromptTemplate
    # the prefix is our instructions
    prefix = """
      You are an expert AI assistant for Autonomous Vehicles. You are an expert in understanding the intent from user queries. 
      Your expertise involves classifying the user's intent based on their queries and their urgency, and ensure that the intent and the urgency exactly matches to the list of intents and urgency list below.

      Below are the possible intents with a brief description

      - Greeting: User greats like Hi, Hey, How are you doing, Whats up, wasspu.

      - Home: Instructs to drive back home, a place to rest.

      - Hungry: When craving something to eat, hungry, need to grab a bite, feel like eating.

      - Restaurant: Instructs to drive to a particular restaurant, place to eat , type of food like tacos, biryani, type of cuisine, Indian, Mexican, Japanese.

      - Coffee Shop: Place to drink something hot, relax, enjoy , cosy space, sip of joe, energising, drink, caffeine, cafe.

      - Hospital: When Feeling Sick, not feeling comfortable, nausea, chest pain, heavy breathing, puckish, stomach pain.

      - Office: Place to work, Place to be productive, Work place, place to work hard.

      - Summon Vehicle: User instructs to be picked up from a particular location, or is ready to go and you need to pick him up.

      - Parking: Instructs you to park, find a parking spot, drop them or stop.

      - Charging Station: When vehicle is low on power and needs to be charge up.

      - Increase: When the user needs to speed up things.

      - Decrease: Just taking things down a notch, relaxing cruise mode engaged.

      - Location: When the user wants to travel somewhere but does not provide the location.

      - Loop: When the user requests to enter into an infinite loop or when the users asks to keep going around.

      - End: When the user ends the conversation with thank you, or you were of great help, bye.

      - None: Choose this if the query does not fall into any of the other intents.

      Below are the two potential urgency with a brief description

      - Urgent: The user is in hurry or rush or is getting late or wants something quick or fast.
      - Normal: If the user is not in rush or not in hurry or not in any kind of emergency

      Task:
      - Your task is to classify the user's intent based on their queries and urgency and then output the intent.
      - When users intent is Hungry, Parking, Decrease, location, help, the urgency is always Normal, but when the intent is Increase the urgency is always Urgent.

      - However, when the user specifies a particular restaurant or cuisine, respond with the nation name that represents that dish along with its intended urgency.

      Use the examples below to develop knowledge, match the intent to the user query, and strictly output intent only.

      Here are some examples
    """

    # The suffix our user input and output indicator
    suffix = """
      Input: {query}
      AI: 
    """

    # Now create the few shot prompt template
    prompt = FewShotPromptTemplate(
        examples=examples,
        example_prompt=example_prompt,
        prefix=prefix,
        suffix=suffix,
        input_variables=['query'],
        example_separator="\n\n"
    )

    # Query the prompt
    query = query
    # print(prompt.format(query=query))

    # Passing prompt to LLM
    chain = LLMChain(llm=llm_1,
                     prompt=prompt,
                     verbose=False)

    result = chain.run(query)

    return result