import streamlit as st
import llmIntegration
import detectionSAM
import os

HOME = os.getcwd()

# streamlit code for viewing document
st.set_page_config(layout="wide",
                   page_title="PCBinsightAI",
                   page_icon="🔭",
                   initial_sidebar_state="collapsed"
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
st.title("PCBinsightAI")
st.subheader(" 🔬Uncover Defects, Enhance Quality.🚀")
st.write("Powered by OpenAI.")
st.markdown(hide_menu, unsafe_allow_html=True)

# Intro ----------------------------------------------------------------------

st.write(
    """
    
    Hi 👋, I'm **:red[Shubham Shankar]**, and welcome to **:green[PCBinsightAI]**! :rocket: Leveraging the latest **:blue[YOLOv10]**, for object detection and zero-shot segmentation using the **:orange[SAM]** model,
    PCBinsightAI ensures precision and reliability in identifying even the smallest imperfections. Integrated chat feature powered by **:violet[GPT]** can be used to gain insights into the causes of damage and explore effective remedies., 
    PCBinsightAI combines powerful technology with user-friendly features to help achieve flawless PCB quality effortlessly.✨
    """
)

st.markdown('---')

st.write(
    """
    ### App Interface!!

    :dog: The web app has an easy-to-use interface. 

    1] **:red[Upload Image]**: Upload an image to perform quality check.
    
    2] **:green[Chat]**: Talk to the intelligent agent about the cause and prevention of damage..

    """
)

st.markdown('---')

st.error(
    """
    Connect with me on [**Github**](https://github.com/RATHOD-SHUBHAM) and [**LinkedIn**](https://www.linkedin.com/in/shubhamshankar/). ✨
    """,
    icon="🧟‍♂️",
)


# Todo: Logo
sidebar_logo = f'{HOME}/logo.jpg'
st.logo(sidebar_logo)

st.markdown('---')

# Todo save file to directory
input_folder = f'{HOME}/inputImage'

def save_uploadedfile(uploadedfile):
    with open(os.path.join(input_folder, uploadedfile.name), "wb") as f:
        f.write(uploadedfile.getbuffer())
        print(st.success("Saved File:{} to input_folder".format(uploadedfile.name)))


datafile = st.file_uploader("Upload Image")

if st.button('Process'):
    if datafile is not None:
        file_details = {"FileName": datafile.name, "FileType": datafile.type}
        save_uploadedfile(datafile)

        with st.spinner('Algorithm Running'):

            # Call detection algorithm
            test_image = os.path.join(input_folder, datafile.name)
            detectionSAM.detection_annotation(test_image)

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.header("Input Image")
                st.image(test_image)

            detection_image = os.path.join(f'{HOME}/runs/detect/predict', datafile.name)
            with col2:
                st.header("Detection")
                st.image(detection_image)

            segmentation_image = f'{HOME}/my_image.jpg'
            with col3:
                st.header("Segmentation")
                st.image(segmentation_image)

            mask_image = f'{HOME}/my_mask.jpg'
            with col4:
                st.header("Mask")
                st.image(mask_image)

with st.sidebar:
    # Todo: LLM Call
    st.subheader('ChatBot.')
    messages = st.container(height=400)
    if query := st.chat_input("Ask your query: "):
        messages.chat_message("user").write(query)
        bot_response = llmIntegration.chatbot(query=query)
        # print(bot_response['result'])
        messages.chat_message("assistant").write(bot_response['result'])

