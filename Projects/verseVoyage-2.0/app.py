import streamlit as st
from models.llama2 import llama2
from models.jurassic import jurassic
from models.gpt import gpt
from models.gemini import gemini

# streamlit code for viewing document
st.set_page_config(layout="wide",
                   page_title="VerseVoyage",
                   page_icon="💗",
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
st.title("VerseVoyage")
st.subheader("Make them laugh🥰, make them sigh🎷, with poetry on the fly🎶.")
st.write("Powered by OpenAI, Amazon Bedrock and Google.")
st.markdown(hide_menu, unsafe_allow_html=True)

# Intro ----------------------------------------------------------------------

st.write(
    """

    Hi 👋, I'm **:red[Shubham Shankar]**, and welcome to my **:green[VerseVoyage]**! :rocket: , This application leverages  **:orange[LLMs]** to generate *poems*.  ✨

    """
)

st.markdown('---')

st.write(
    """
    ### App Interface!!

    :dog: The web app has an easy-to-use interface. 
    
    1] **:red[Choose Model]**: From the sidebar, Select a provider of your choice.
    
    2] **:green[Choose Model]**: From the sidebar, Select the model of your choice.

    3] **:orange[Generate]**: Plug in your API Key.
    
    4] **:green[Generate]**: Shoot a topic, and the model will compose poem.

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

# Todo: Choose the Provider
st.sidebar.title("Select A Provider 🧞‍♂️")
model = st.sidebar.radio('Pick One: ', ['OpenAI: gpt-3.5-turbo', 'AWS-Bedrock', 'Google: gemini-pro'])

if model == 'OpenAI: gpt-3.5-turbo':
    st.sidebar.title("OpenAI 🧠")
    model_name = st.sidebar.selectbox('Model of choice?', ('gpt-3.5-turbo', 'gpt-4'))

    st.title("API Keys 🔐")
    with st.form('myform', clear_on_submit=True):

        user_input = st.text_input('Poem About?', 'My Beautiful Girlfriend')

        openai_api_key = st.text_input('OPENAI_API_KEY', type='password', disabled=not user_input)
        submitted = st.form_submit_button('Generate', disabled=not user_input)

        if user_input and submitted:
            try:
                st.snow()
                with st.spinner('Wait for it...'):
                    if model_name == 'gpt-3.5-turbo':
                        obj = gpt()
                        response = obj.gpt(user_input=user_input, openai_api_key=openai_api_key)
                        st.text_area("Here you go: ",
                                     response)
                    else:
                        st.info("🏃🏻‍♂️... Work in Progress.")

                    st.balloons()
            except Exception:
                st.error('❌Access Denied: Invalid API')

elif model == 'AWS-Bedrock':
    st.sidebar.title("Amazon Bedrock Models 🗿")
    model_name = st.sidebar.selectbox('Model of choice?', ('Llama-2', 'Jurassic-2'))


    st.title("API Keys 🔐")
    with st.form('myform', clear_on_submit=True):

        user_input = st.text_input('Poem About?', 'My Beautiful Girlfriend')

        AWS_ACCESS_KEY_ID = st.text_input('AWS_ACCESS_KEY_ID', type='password', disabled=not user_input)
        AWS_SECRET_ACCESS_KEY = st.text_input('AWS_SECRET_ACCESS_KEY', type='password', disabled=not user_input)
        submitted = st.form_submit_button('Generate', disabled=not user_input)

        if user_input and submitted:
            try:
                st.snow()
                with st.spinner('Wait for it...'):
                    if model_name == 'Llama-2':
                        obj = llama2()
                        response = obj.llama2(user_input=user_input, AWS_ACCESS_KEY_ID=AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY=AWS_SECRET_ACCESS_KEY)
                        st.text_area("Here you go: ",
                                     response)
                    else:
                        obj = jurassic()
                        response = obj.jurassic(user_input=user_input, AWS_ACCESS_KEY_ID=AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY=AWS_SECRET_ACCESS_KEY)
                        st.text_area("Here you go: ",
                                     response)

                    st.balloons()
            except Exception:
                st.error('❌Access Denied: Invalid API')

else:
    st.sidebar.title("Google Gemini ♊")
    st.sidebar.write("💁🏻Activate model")
    model_name = st.sidebar.toggle('gemini-pro')

    st.title("API Keys 🔐")
    with st.form('myform', clear_on_submit=True):

        user_input = st.text_input('Poem About?', 'My Beautiful Girlfriend')

        google_api_key = st.text_input('GOOGLE_API_KEY', type='password', disabled=not user_input)
        submitted = st.form_submit_button('Generate', disabled=not user_input)

        if user_input and submitted:
            try:
                st.snow()
                with st.spinner('Wait for it...'):
                    if model_name:
                        obj = gemini()
                        response = obj.gemini(user_input=user_input, google_api_key=google_api_key)
                        st.text_area("Here you go: ",
                                     response)
                    else:
                        st.warning('🌻 Model Inactive: Activate the model for use')

                    st.balloons()
            except Exception:
                st.error('❌Access Denied: Invalid API')




st.markdown('---')

# Copyright information
st.markdown(
    """
        © Copyright 2024 Shubham Shankar 
    """
)