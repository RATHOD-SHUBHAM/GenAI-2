# Installation

# ----install SAM, Stable Diffusion and libraries
!pip -q install diffusers transformers scipy segment_anything

# ------install GroundingDINO, DINO weights
# 1.Clone the GroundingDINO repository from GitHub.
!git clone https://github.com/IDEA-Research/GroundingDINO.git

# 2.Change the current directory to the GroundingDINO folder.
%cd GroundingDINO

# 3.Install the required dependencies in the current directory.
!pip -q install -e .

# 4. Download pre-trained model weights.
%mkdir weights
%cd weights
# Also add sam weights
!wget -q https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth
!wget -q https://github.com/IDEA-Research/GroundingDINO/releases/download/v0.1.0-alpha/groundingdino_swint_ogc.pth
%cd ..


# If using GPU

In app.py change:

    1] Device Setting
    device = "cpu"  # Change to CUDA for GPU
    2] In stable diffusion pipeline change torch_dtype
    pipe = StableDiffusionInpaintPipeline.from_pretrained("stabilityai/stable-diffusion-2-inpainting", torch_dtype=torch.float16,).to(device) # For GPU

After cloning GroudningDino repo change
    1] cd GroundingDINO/groundingdino/util/inference.py
    2] Go to predict function and change
        device: str = "CUDA".