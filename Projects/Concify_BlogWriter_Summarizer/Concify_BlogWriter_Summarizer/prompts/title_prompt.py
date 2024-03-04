from langchain.prompts import PromptTemplate


template = """
    You are a experienced and creative blog writer.
    You will be provided with a topic and you need to provide an interesting blog title for that particular topic.
    The title should create curiosity among the readers.
    Return the title only
    
    topic : {topic}
    title : 
"""

prompt = PromptTemplate(
    input_variables = ['topic'],
    template=template
)

prompt.save('title_prompt.json')