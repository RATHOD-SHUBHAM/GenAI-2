import streamlit as st
from backend_blogger import Backend_Blogger

# streamlit code for viewing document
st.set_page_config(layout="wide",
                   page_title="Concisify",
                   page_icon="✍️",
                   )

# hide hamburger and customize footer
hide_menu = """
    <style>

    #MainMenu {
        visibility:hidden;
    }
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        color: grey;
        text-align: center;
    }
    
    </style>
    
    <div class="footer">
        <p>'With 🫶️ from Shubham Shankar.'</p>
    </div>

"""


# Styling ----------------------------------------------------------------------
st.image("icon.jpg", width=85)
st.title("Concisify")
st.subheader(" ✍️ Write Long, Summarize Short with Powerful AI 🧠.")
st.write("Powered by OpenAI.")
st.markdown(hide_menu, unsafe_allow_html=True)


# Intro ----------------------------------------------------------------------

st.write(
    """

    Hi 👋, I'm **:red[Shubham Shankar]**, and welcome to my **:green[Concisify]**! :rocket: This app makes use of **:blue[Large Language Model]**, such as **:orange[GPT-3.5 Turbo]** as well as strategies
    such as **:violet[Prompt Serialization]** which allows us to have a **dynamic prompt** and a **:violet[Sequential Chain]** to link **Multiple Workflow** together, 
    to  produce  **Curiosity Pieking Title**, **Interesting Blogs**, and a **Brief Summary** of the blog✨
    """
)

st.markdown('---')

st.write(
    """
    ### App Interface!!

    :dog: The web app has an easy-to-use interface. 

    1] **:red[Topic]**: Enter the topic on which you wish the blog to be generated.

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


# Todo Main Func
if __name__ == '__main__':
    st.subheader(" Write Long, Summarize Short.")
    with st.form("my_form"):

        topic = st.text_input('Topic','Large Language Models')
        openai_api_key = st.text_input('OPENAI_API_KEY', type='password', disabled=not topic)
        submitted = st.form_submit_button("Submit")

        if topic and submitted:
            try:
                with st.spinner('Generating Your Blog in a moment...'):
                    obj = Backend_Blogger()
                    response = obj.backend_blogger(topic=topic,openai_api_key=openai_api_key)
                    st.text_input('Title',response['title'])
                    st.divider()
                    with st.expander('Script'):
                        st.write(response['script'])
                    st.divider()
                    with st.expander('Summary'):
                        st.write(response['summary'])
            except Exception:
                st.error('❌Access Denied: Invalid API')
