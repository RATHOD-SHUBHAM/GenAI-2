# GenAI-2
LLM
---
### Note: [GenAI-1](https://github.com/RATHOD-SHUBHAM/GenAI-1) repository can be found here.

---

# Projects

## StableSAM:

In computer vision, object recognition and segmentation are crucial tasks. However, they often necessitate manual annotation of bounding boxes or segmentation masks, which can be time-consuming and expensive.

So? 

Forget manual image editing! Recent advancements in AI models are unlocking entirely new ways to interact with images and videos using just text commands. 

This exciting approach leverages the strengths of three key models:

    1.	Grounding DINO: Identifies objects within the image based on your text description.
    2.	Meta's SAM: Segments the identified objects, creating precise masks.
    3.	Stable Diffusion: Modifies the image based on your further text instructions, seamlessly integrating the new elements.
     
This powerful trio opens a world of possibilities:

    •	Faster Design Prototyping: Visualize ideas instantly, enabling quicker feedback and iteration cycles.
    •	Inclusive Content Creation: Easily translate and localize images for broader audiences.
    •	Streamlined Editing: Edit images and videos efficiently with text prompts, ideal for both individual creators and large-scale content management.
    •	Seamless Object Manipulation: Effortlessly identify and replace objects within an image, offering endless creative possibilities.



<img width="2193" alt="Screenshot 2024-02-03 at 7 38 37 PM" src="https://github.com/RATHOD-SHUBHAM/GenAI-2/assets/58945964/362c4bf3-0006-4eb8-a10a-1d1a6f260d75">

---

## Intent Detection

    - Creating an AI chatbot involves more than just using a model API and adding context with our data. We should also consider the various intents users might have and how to manage them.

Why do you need it?
```
let's say that we have defined 5 intent categories: "Order Status", "Product Information", "Payments", "Returns" and "Feedback”.

For each category, there should be a distinct step where the LLM-powered chatbot, figures out the user's intent. It does this by placing the user's question into the right category. After identifying the intent, the chatbot can then take the next appropriate actions for that particular category.

Having separate steps for the prompts and intent handlers is useful because each of your intents might need to do different actions. For example: “Returns” might need to be handled by an external service/API that a handler action should call, and the handler for “Product information” might just call an LLM and a context doc to answer with text response. Also, adding too many instructions in one prompt can also influence the performance.

Identifying these intents accurately allows the chatbot to respond better, call an external API or route the query to the correct personnel for further assistance.
```

<img width="1046" alt="Screenshot 2024-02-04 at 7 14 32 PM" src="https://github.com/RATHOD-SHUBHAM/GenAI-2/assets/58945964/066e2d1b-f874-41f5-ab15-019c6cdb2c20">

This amazing [article](https://www.vellum.ai/blog/how-to-build-intent-detection-for-your-chatbot#:~:text=For%20each%20category%2C%20there%20should,actions%20for%20that%20particular%20category.) discusses Intent Detection in detail.

---