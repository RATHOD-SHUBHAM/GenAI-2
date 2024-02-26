from langchain.prompts import PromptTemplate

template = """
    You are a experienced and creative blog writer.
    You will be provided with a blog title and you need to write an interesting blog related to that title.
    Keep your writing elegant and professional.
    The blog audience mainly consist of Engineers and Students,and the script should be less that 1000 word.
    Return the blog script only

    title : {title}
    script : 
"""

prompt = PromptTemplate(
    input_variables=['title'],
    template=template
)

prompt.save('script_prompt.json')