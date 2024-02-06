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

## QueryVerse
QueryVerse, a web application designed to be our personal knowledge hub, powered by the cutting-edge capabilities of Google Gemini Pro, Langchain, Vector DB, and Streamlit.

**What can QueryVerse do?**

QueryVerse offers three distinct applications, each leveraging the popwer of large language models (LLMs) to engage in meaningful interactions:

    * Q&A: Unleash your curiosity! Ask QueryVerse anything, across diverse topics, and receive informative, comprehensive answers. Its knowledge base is vast and continuously expanding, ensuring you stay informed and empowered.
    
    * Vision: See beyond the pixels! Upload an image and QueryVerse will analyze it, providing insights and details, answering your questions with remarkable accuracy. Imagine understanding complex visuals with just a click!
    
    * Chatbot: Dive deep into your documents! Upload documents and ask QueryVerse questions directly related to their content. Its contextual understanding allows it to answer with precision, streamlining our information retrieval process.

**Technical Power for Powerful Interactions:**

At the heart of QueryVerse lies a sophisticated blend of technologies:

    * Google Gemini Pro: This powerhouse LLM delivers exceptional natural language processing, enabling QueryVerse to understand our questions and respond coherently.
    
    * Langchain: This framework seamlessly combines different AI models, allowing QueryVerse to leverage the strengths of various specialists for comprehensive problem-solving.
    
    * Vector DB: This efficient database stores and retrieves information with impressive speed, ensuring QueryVerse delivers answers rapidly.
    
    * Streamlit: This user-friendly platform creates a clean and intuitive web interface, making QueryVerse accessible and enjoyable to use.

**Business Value: A World of Possibilities:**

LLMs transcend mere functionality, offering tangible value across various domains:

    Customer Service: Enhance customer experiences by providing instant, 24/7 support through LLM's Q&A and Chatbot features.
    
    Education: Foster deeper learning by empowering us with a personalized knowledge assistant.
    
    Content Creation: Streamline research and content generation by leveraging LLM's ability to process information and answer questions creatively.
    
    Data Analysis: Extract insights from unstructured data efficiently with LLM's Vision and Chatbot capabilities.


<img width="2301" alt="Screenshot" src="https://github.com/RATHOD-SHUBHAM/GenAI-2/assets/58945964/a90dfcb7-b6f6-414b-900b-f4d5ad117ad2">