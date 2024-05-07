# Todo: Import Libraries
import streamlit as st
import os
from process_file import VideoProcess

# streamlit code for viewing document
st.set_page_config(layout="wide",
                   page_title="SoundSight Synthesizer",
                   page_icon="🙉",
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
st.title("SoundSight Synthesizer")
st.subheader("Unlock the unseen: where audio and video converge to reveal the full context of every moment.")
st.write("Powered by OpenAI, Langchain & Streamlit.")
st.markdown(hide_menu, unsafe_allow_html=True)

# Intro ----------------------------------------------------------------------

st.write(
    """

    Hi 👋, I'm **:red[Shubham Shankar]**, and welcome to my **:green[SoundSight Synthesizer]**! :rocket: , This application leverages  **:orange[LLMs]** to decode the world around you cause *every video tells a richer story*.  ✨

    """
)

st.markdown('---')

st.write(
    """
    ### App Interface!!

    :dog: The web app has an easy-to-use interface. 

    1] **:red[Upload Video]**: Upload a video of your choice.

    2] **:green[Audio Transcript]**: An audio transcript is generated.

    3] **:orange[Event]**: Content in the video is displayed.
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

# Todo: Save the file
def save_uploadedfile(uploadedfile):
    with open(os.path.join("output", uploadedfile.name), "wb") as f:
        f.write(uploadedfile.getbuffer())

    return st.success("Saved File:{} to output".format(uploadedfile.name))


# Todo: Main File
if __name__ == '__main__':
    obj = VideoProcess()

    datafile = st.file_uploader("Upload video", type=['mov', 'mp4'])

    if datafile is not None:
        file_details = {"FileName": datafile.name, "FileType": datafile.type}
        save_uploadedfile(datafile)

        if datafile.name and st.button('Run'):

            with st.spinner("Processing ..."):

                output_dir = 'output'

                input_file_path = os.path.join(output_dir, datafile.name)

                transcript, response = obj.video_GPT(input_file_path)# pass the input to video processor

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.header("Raw Video")
                    st.video(input_file_path, format="video/mp4")

                with col2:
                    st.header("Audio Transcript of Raw Video")
                    st.write(transcript)

                with col3:
                    st.header("Event taking place")
                    st.write(response)






