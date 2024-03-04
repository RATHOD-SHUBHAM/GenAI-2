from langchain.prompts import PromptTemplate

template = """
    You are an professional educational agent. 
    Your task is to summarize the given blog script that is provided to you.
    You return the summary as bullet point and also gave a points on import topic in the end.
    Main audience for this summary section will be students.

    script : {script}
    summary : 
"""

prompt = PromptTemplate(
    input_variables=['script'],
    template=template
)

prompt.save('summary_prompt.json')