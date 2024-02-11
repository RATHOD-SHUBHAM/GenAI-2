# Todo: Import Libraries
from datetime import datetime
# from datetime import timedelta
import streamlit as st
import os
import google.generativeai as genai
import csv
import pandas as pd
from PIL import Image

# streamlit code for viewing document
st.set_page_config(layout="wide",
                   page_title="Q_&_A",
                   page_icon="👾",
                   )

# hide hamburger and customize footer
hide_menu = """
    <style>

    #MainMenu {
        visibility:hidden;
    }

    footer{
        visibility:visible;
    }

    footer:after{
        content: 'With 🫶️ from Shubham Shankar.';
        display:block;
        position:relative;
        color:grey;
        padding;5px;
        top:3px;
    }
    </style>

"""
# Styling ----------------------------------------------------------------------

st.image("icon.jpg", width=85)
st.title("Queryverse")
st.subheader("Answer Questions, Decode Images, Gain Insights.")
st.write("All with LLM - Powered by Google.")
st.markdown(hide_menu, unsafe_allow_html=True)

st.markdown('---')

st.write(
    """
    ### App Interface!!

    :dog: The web app has an easy-to-use interface. 

    **:green[Q_A Demo]**: Ask questions you feel like and get a response. - (* limited to pretrained knowledge)

    """
)

st.markdown('---')

st.error(
    """
    Connect with me on [**Github**](https://github.com/RATHOD-SHUBHAM) and [**LinkedIn**](https://www.linkedin.com/in/shubhamshankar/). ✨
    """,
    icon="🧟‍♂️",
)

st.markdown('---')





# Todo: Load the API
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

# Todo: Access the Keys
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# Todo: Config api key
genai.configure(api_key=GOOGLE_API_KEY)


q_a_file = '/Users/shubhamrathod/PycharmProjects/multiModel_with_GeminiPro/Q_&_A.csv'


# Todo: Write data to CSV file
def write_data(query, answer):
    try:
        current_time = datetime.now()
        # expiration_time = current_time + timedelta(days=1)  # delete after a day.

        # Store the data in csv
        # data = [query, answer, expiration_time.strftime('%y-%m-%d')]
        data = [query, answer, current_time]

        # Append the data to the CSV file
        with open(q_a_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data)

    except Exception as e:
        st.error(f"Error while storing the data: {e}")


# Todo: Read and Dispaly from the CSV
def read_and_display():
    try:
        with open(q_a_file, mode='r') as file:

            reader = csv.reader(file)

            historic_data = list(reader)

        return historic_data

    except FileNotFoundError:
        return []


# Updated and more powerful prompt
prompt = """

    You are a Intelligent and Knowledgeable Agent , 
    You respond clearly and concisely to the user's query, drawing from various fields of knowledge. 
    Also use bullet Points & Paragraphs when required to be more precise and accurate.
    
    Donot include html elements in your response

"""


# Todo: Ask user to load the API

# Todo: Load the models
def gemini_pro(input_text, prompt):
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content([input_text, prompt])
        return response.text
    except Exception as e:
        st.error(f"Error occurred during the model call: {e}")


if __name__ == '__main__':
    st.subheader("Ask me anything you want to know")
    input_text = st.text_input('Question: ', 'What is Generative AI ?')

    # Check if the "Send Message" button is clicked
    if st.button("Ask"):
        if not input_text:
            st.warning("please ask a question.")
        else:
            # Generate response
            response = gemini_pro(input_text, prompt)

            # Display response
            st.subheader("Answer:")
            st.write(response)

            # Store question in CSV file
            write_data(input_text, response)

    # Display last 5 rows of question history with column names
    historic_data = read_and_display()
    if historic_data:
        st.subheader("Recent Search's")

        # Convert the list of lists to a DataFrame
        # df = pd.DataFrame(historic_data, columns=["Question","Answer", "Expire On"])
        df = pd.DataFrame(historic_data, columns=["Question", "Answer", "Time of query"])

        # Display the last 5 rows in reverse order
        st.write(df.tail(50).iloc[::-1])
    else:
        st.info("No search history is available yet.")
