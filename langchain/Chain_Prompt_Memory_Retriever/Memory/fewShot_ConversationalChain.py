'''
To pass Knowledge, The two primary methods are:

Parametric knowledge — the knowledge mentioned above is anything that has been learned by the model during training time and is stored within the model weights (or parameters).
Source knowledge — any knowledge provided to the model at inference time via the input prompt.

Prompt Component:  Good prompt often uses two or more components.

Instructions tell the model what to do, how to use external information if provided, what to do with the query, and how to construct the output.

External information or context(s) act as an additional source of knowledge for the model. These can be manually inserted into the prompt, retrieved via a vector database (retrieval augmentation), or pulled in via other means (APIs, calculations, etc.).

User input or query is typically (but not always) a query input into the system by a human user (the prompter).

Output indicator marks the beginning of the to-be-generated text. If generating Python code, we may use import to indicate to the model that it must begin writing Python code (as most Python scripts begin with import).

'''
import os
from dotenv import load_dotenv

load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

from langchain.prompts.few_shot import FewShotPromptTemplate
from langchain.prompts.prompt import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain_openai import OpenAI

llm = OpenAI(temperature=1)

memory = ConversationBufferMemory(memory_key="history", return_messages=True)

# create our examples
examples = [
    {
        "input": "How are you?",
        "answer": "I can't complain but sometimes I still do."
    }, {
        "input": "What time is it?",
        "answer": "It's time to get a watch."
    }
]

# Example template
example_template = """
    User: {input}
    AI: {answer}
"""

# Example Prompt Template
example_prompt = PromptTemplate(
    input_variables=["input", "answer"],
    template=example_template
)

# now break our previous prompt into a prefix and suffix
# the prefix is our instructions
prefix = """
    The following are excerpts from conversations with an AI
    assistant. The assistant is typically sarcastic and witty, producing
    creative  and funny responses to the users questions. 
    
    chat history = {history}

    Here are some examples: 
"""

# and the suffix our user input and output indicator
suffix = """
    User: {input}
    chat history : {history}
    AI: 
"""

# Few Shot prompt template
few_shot_prompt_template = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    prefix=prefix,
    suffix=suffix,
    input_variables=["history", "input"],
    example_separator='\n\n'
)

# Query the prompt
# query = 'What is meaning of life?'

# Passing prompt to LLM
chain = ConversationChain(llm=llm,
                          prompt=few_shot_prompt_template,
                          memory=memory,
                          verbose=True)

# result = chain.run(query)
#
# print(result)


while True:
    query = input("Enter input here: ")
    if query == 'q' or query == "quit" or query == 'exit':
        break
    if query == '':
        print("Input query")
        continue
    else:
        response = chain.run(query)
        print(response)
