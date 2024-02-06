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
                   page_title="Vision",
                   page_icon="🕶",
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

    1] **:green[Upload Image]**: Upload the image you want to query.

    2] **:red[Query]**: Ask a question about the image.

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


# Todo: Load the model
def gemini_pro_vision(image, prompt):
    try:
        model = genai.GenerativeModel('gemini-pro-vision')
        response = model.generate_content([image, prompt])
        return response.text
    except Exception as e:
        st.error(f"Error occurred during the model call: {e}")


# Function to prepare image data for Gemini Pro Vision API
def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")


def save_uploadedfile(uploadedfile):
    with open(os.path.join("inputImage", uploadedfile.name), "wb") as f:
        f.write(uploadedfile.getbuffer())
    return st.success("Saved File to inputImage")


if __name__ == '__main__':
    datafile = st.file_uploader("Upload image: ", type=['png', 'jpeg', 'jpg'])

    if datafile is not None:
        file_details = {"FileName": datafile.name, "FileType": datafile.type}
        st.write(datafile)
        save_uploadedfile(datafile)

        # Process the image and get user input for custom prompt
        image = Image.open(datafile)
        st.image(image, caption="Uploaded Image.", use_column_width=True)

        prompt = st.text_area("Ask me anything about the image: ",
                              "Examine the uploaded picture and provide an in-depth analysis that include, the objects present, its contextual details, and significant characteristics."
                              "Give all the information about the image as well, mentioning any unusual characteristics."
                              )

        if st.button("Get Information"):
            image_data = input_image_setup(datafile)
            response = gemini_pro_vision(image_data[0], prompt)
            st.subheader("The Response is")
            st.write(response)
