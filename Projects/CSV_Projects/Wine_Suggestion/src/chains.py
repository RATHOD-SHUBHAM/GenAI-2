from langchain.chains import LLMChain, SequentialChain
from langchain.prompts import ChatPromptTemplate
from langchain_openai import OpenAIEmbeddings
from langchain_openai import OpenAI
from langchain.output_parsers import ResponseSchema, StructuredOutputParser, RetryOutputParser
from dotenv import load_dotenv
import os

load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')


class Chain:
    def __init__(self):
        self.llm = OpenAI()

    def build_query_chain(self):
        query_string = [
            ResponseSchema(
                name="query_string",
                description="The string used to query the vector database for wine options"
            )
        ]
        output_parser = StructuredOutputParser.from_response_schemas(query_string)

        response_format_instruction = output_parser.get_format_instructions()

        prompt = ChatPromptTemplate.from_template(
            """
                You are a expert wine sommelier.
                Your goal is to select a wine from the database to recommend to the user.
                
                Take a breath and understand the following user preferences:
                taste: {taste}
                experience level:{experience}
                wine color: {wine_color}
                flavor: {flavor}
                pairing: {pairing}
                complement: {complement}
                
                Now create a string that will be used to do a similarity search on vector database containing wine description.
                To build better queries for similarity search ensure they are specific, utilize relevant features or descriptors.
                
                {response_format_instruction}
            """
        )

        # Todo: LLMChain doesnot accept input variable
        llm_chain = LLMChain(
            llm=self.llm,
            prompt=prompt,
            output_key='query'
        )

        # Todo: To pass input to LLMChain we can pass the input to sequential chain which internally will pass it to LLMChain
        chain = SequentialChain(
            chains=[llm_chain],
            input_variables=["taste", "experience", "wine_color", "flavor", "pairing", "complement"] + [
                "response_format_instruction"],
            output_variables=["query"],
            verbose=False,
        )

        return chain, response_format_instruction, output_parser

    def build_recommendation_chain(self):
        recommendation_string = ResponseSchema(
            name="recommendation",
            description='The recommended wine name.'
        )

        explanation_string = ResponseSchema(
            name='explanation',
            description='The explanation of the selected recommendation.'
        )

        output_parser = StructuredOutputParser.from_response_schemas([
            recommendation_string,
            explanation_string
        ])

        response_format_instructions = output_parser.get_format_instructions()

        # Previously we queried the db based on user choice
        # Now we query the LLM based on user choice and the wine choice which matches the best
        prompt = ChatPromptTemplate.from_template(
            """
                You are an expert wine sommelier. 
                Your goal is to select a wine from the options bellow to recommend to the user.
                
                Take a breath and understand the following user preferences:
                taste: {taste}
                experience level:{experience}
                wine color: {wine_color}
                flavor: {flavor}
                pairing: {pairing}
                complement: {complement}
        
                Now take a breath and understand the wine options:
                Option 1:
                {wine_1}
                Option 2:
                {wine_2}
                Option 3:
                {wine_3}
                Option 4:
                {wine_4}
        
                Now select the best wine to recommend to this user, 
                Also make sure to address the user as your.
                You are an talkative and you talk to user with utmost respect and appreciate their choice.
        
                {response_format_instructions}
            """
        )

        llm_chain = LLMChain(
            llm=self.llm,
            prompt=prompt,
            output_key = "recommendation"
        )

        chain = SequentialChain(
            chains = [llm_chain],
            input_variables=["taste", "experience", "wine_color", "flavor", "pairing", "complement", "wine_1", "wine_2", "wine_3", "wine_4"] + ["response_format_instructions"],
            output_variables=["recommendation"],
            verbose=False,
        )

        return chain, response_format_instructions, output_parser
