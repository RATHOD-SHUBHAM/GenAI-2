import streamlit as st


# streamlit code for viewing document
st.set_page_config(layout="wide",
                   page_title="Home",
                   page_icon="👋",
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

# Intro ----------------------------------------------------------------------

st.write(
    """

    Hi 👋, I'm **:red[Shubham Shankar]**, and welcome to my **:green[Queryverse]**! :rocket: This app makes use of **:blue[Large Language Model]**, such as **:orange[Gemini Pro]** model, and **:blue[Gemini Pro Vision]** model, 
    to  **Get Answers**, **Explore Images**, **Gain Knowledge & Understand content** of the document and then reply to **:violet[User Query]** appropriately.  ✨

    """
)

st.markdown('---')

st.write(
    """
    ### App Interface!!

    :dog: The web app has an easy-to-use interface. 
    
    Choose any task you want to perform from the side bar :

    1] **:green[Q_A Demo]**: Ask questions you feel like and get a response. - (* limited to pretrained knowledge)

    2] **:violet[Vision Demo]**: Upload an Image, query it.
    
    3] **:red[Chat Bot Demo]**: Ask context specific question to the agent. - (* domain specific)

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

# Copyright information
st.markdown(
    """
        © Copyright 2024 Shubham Shankar 
    """
)
