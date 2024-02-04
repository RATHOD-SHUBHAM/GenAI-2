# SAM
from segment_anything import SamPredictor, sam_model_registry

# Inpainting
from diffusers import StableDiffusionInpaintPipeline
from PIL import Image


# Grounding Dino
from groundingdino.util.inference import load_model, load_image, predict, annotate
from GroundingDINO.groundingdino.util import box_ops

import torch
import numpy as np
import streamlit as st
import os



# Streamlit Config ----------------------------------------------------------------------

# streamlit code for viewing document
st.set_page_config(layout="wide")


# hide hamburger and customize footer
hide_menu= """
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
st.title("StableSam")
st.subheader("Detect - Segment -> Change")
st.markdown(hide_menu, unsafe_allow_html=True)

# Intro ----------------------------------------------------------------------

st.write(
    """

    Hi 👋, I'm **:red[Shubham Shankar]**, and welcome to **:green[StableSAM Application]**! :rocket: This program makes use of **:blue[GroundingDino]** to perform zero shot object detection & **:orange[SAM model]** to generate segmentation, 
    & to change the object it uses **:violet[Stable Diffusion]** .  ✨

    """
)

st.markdown('---')

st.write(
    """
    ### Model Pipeline!!

    :sloth:: Image editing is possible using only text commands. 

    '''
    
    Models like **Segment Anything Model (SAM), Stable Diffusion, and Grounding DINO** have made it possible. Together, they create a powerful workflow that seamlessly combines image zero shot detection, segmentation, and inpainting. 
        
        1] We first use Grounding DINO for zero shot object detection based on the text input. Using the predict function from GroundingDINO, we obtain the boxes, logits, and phrases for our image. We then annotate our image using these results.
        
        2] Then, we will use SAM to extract masks from the bounding box.
        
        3] Then, we modify the image based on a text prompt using Stable Diffusion. The pipe function from Stable Diffusion is used to inpaint the areas identified by the mask with the contents of the text prompt.
    '''
    """
)

st.image("pipeline.png")

st.markdown('---')

st.write(
    """
    ### App Interface!!

    :dog: The web app has an easy-to-use interface. 

    1] **:green[Upload File]**: Upload a Image you want to perform changes.

    2] **:violet[Detect Prompt]**: Enter the name of object you want to change.
    
    3] **:orange[Change Prompt]**: Enter the name to which you want the object to change.
    
     4] **:red[Run]**: Generate output.

    """
)
st.markdown('---')

st.warning(
    """
    * Change device to GPU for faster execution
    * In 'GroundingDINO/groundingdino/util/inference.py' change device: str = "cuda", # For GPU✨
    """,
    icon="🌶️",
)

st.markdown('---')

st.error(
    """
    Connect with me on [**Github**](https://github.com/RATHOD-SHUBHAM) and [**LinkedIn**](https://www.linkedin.com/in/shubhamshankar/). ✨
    """,
    icon="🧟‍♂️",
)

st.markdown('---')



# Model Serving ----------------------------------------------------------------------

# Device Setting
device = "cpu"  # Change to CUDA for GPU

# SAM Parameters
model_type = "vit_h"
predictor = SamPredictor(sam_model_registry[model_type](checkpoint="GroundingDINO/weights/sam_vit_h_4b8939.pth").to(device=device))

# Stable Diffusion
# pipe = StableDiffusionInpaintPipeline.from_pretrained("stabilityai/stable-diffusion-2-inpainting", torch_dtype=torch.float16,).to(device) # For GPU
pipe = StableDiffusionInpaintPipeline.from_pretrained("stabilityai/stable-diffusion-2-inpainting", torch_dtype=torch.float32,).to(device)
# Grounding DINO
groundingdino_model = load_model("GroundingDINO/groundingdino/config/GroundingDINO_SwinT_OGC.py", "GroundingDINO/weights/groundingdino_swint_ogc.pth")


# Todo: Save Uploaded Image
def save_uploadedfile(uploadedfile):
    with open(os.path.join("inputDir", uploadedfile.name), "wb") as f:
        f.write(uploadedfile.getbuffer())
    return st.success("Saved File to inputDir")

# Todo: Pipeline
def show_mask(mask, image, random_color=True):
    if random_color:
        color = np.concatenate([np.random.random(3), np.array([0.8])], axis=0)
    else:
        color = np.array([30 / 255, 144 / 255, 255 / 255, 0.6])

    h, w = mask.shape[-2:]

    mask_image = mask.reshape(h, w, 1) * color.reshape(1, 1, -1)

    annotated_frame_pil = Image.fromarray(image).convert("RGBA")

    mask_image_pil = Image.fromarray((mask_image.cpu().numpy() * 255).astype(np.uint8)).convert("RGBA")

    return np.array(Image.alpha_composite(annotated_frame_pil, mask_image_pil))

def process_boxes(boxes, src):
    H, W, _ = src.shape
    boxes_xyxy = box_ops.box_cxcywh_to_xyxy(boxes) * torch.Tensor([W, H, W, H])
    return predictor.transform.apply_boxes_torch(boxes_xyxy, src.shape[:2]).to(device)

def edit_image(path, item, prompt, box_threshold, text_threshold):
    src, img = load_image(path)
    boxes, logits, phrases = predict(
        model=groundingdino_model,
        image=img,
        caption=item,
        box_threshold=box_threshold,
        text_threshold=text_threshold
    )
    predictor.set_image(src)
    new_boxes = process_boxes(boxes, src)
    masks, _, _ = predictor.predict_torch(
        point_coords=None,
        point_labels=None,
        boxes=new_boxes,
        multimask_output=False,
    )
    img_annotated_mask = show_mask(masks[0][0].cpu(),
        annotate(image_source=src, boxes=boxes, logits=logits, phrases=phrases)[...,::-1]
    )
    return pipe(prompt=prompt,
        image=Image.fromarray(src).resize((512, 512)),
        mask_image=Image.fromarray(masks[0][0].cpu().numpy()).resize((512, 512))
    ).images[0]


if __name__ == '__main__':
    datafile = st.file_uploader("Upload Image")
    if datafile is not None:
        file_details = {"FileName": datafile.name, "FileType": datafile.type}
        st.write(file_details)
        save_uploadedfile(datafile)

        detect_prompt = st.text_input('Object to be detected', 'boat')
        change_prompt = st.text_input('Object of change', 'a red car')

        if st.button('Run'):
            with st.spinner('Processing ...'):

                path = 'inputDir/'+datafile.name
                edited_image = edit_image(path, detect_prompt, change_prompt, 0.3, 0.2)
                edited_image.save('output.png')

            col1, col2 = st.columns(2)

            with col1:
                st.header("Input Image")
                st.image(path)

            with col2:
                st.header("Output Image")
                st.image("output.png")


