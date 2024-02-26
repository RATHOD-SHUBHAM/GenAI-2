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
from langchain.chains import LLMChain
from langchain_openai import OpenAI

llm = OpenAI(temperature = 1)

# create our examples
examples = [
    {
        "query": "How are you?",
        "sarcasm":"High",
        "answer": "I can't complain but sometimes I still do."
    }, {
        "query": "What time is it?",
        "sarcasm":"Low",
        "answer": "It's time to get a watch."
    }
]

# Example template
example_template = """
    User: {query}
    Sarcasm-Level:{sarcasm}
    AI: {answer}
"""

# Example Prompt Template
example_prompt = PromptTemplate(
    input_variables=["query", "sarcasm", "answer"],
    template=example_template
)

# now break our previous prompt into a prefix and suffix
# the prefix is our instructions
prefix = """
    The following are excerpts from conversations with an AI
    assistant. The assistant is typically sarcastic and witty, producing
    creative  and funny responses to the users questions. Here are some
    examples: 
"""

# and the suffix our user input and output indicator
suffix = """
    User: {query}
    Sarcasm-Level: {sarcasm}
    AI: 
"""

# Few Shot prompt template
few_shot_prompt_template = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    prefix=prefix,
    suffix=suffix,
    input_variables=["query", "sarcasm"],
    example_separator='\n\n'
)

# Query the prompt
query = 'What is meaning of life?'
sarcasm = 'High'
print(few_shot_prompt_template.format(query=query, sarcasm = sarcasm))

# Passing prompt to LLM
chain = LLMChain(llm=llm,
                 prompt=few_shot_prompt_template,
                 verbose=False)

result = chain.invoke({'query':query, 'sarcasm':sarcasm})
#
print(result)
print(result['text'])