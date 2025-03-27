from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import base64

encoded_image = None
with open("/Users/gabrielsabaini/Downloads/Augmented_Dataset/Sixray/images/P00003flip-1.jpg", "rb") as image:
    encoded_image = image

if encoded_image == None:
    exit(0)

llama_vision_template = """"
You are a security guard that checks weapons in an airport. You have to analyze the sent image to check for dangerous weapons. You have to give short answers to your assistant, so it can call the security if some weapon is found by you.

image: {image}
"""

llamaVisionMessages = [
    {
        "role": "You are a security guard that checks weapons in an airport. You have to check the base64 encoded image and tell to your assistant the result of the analysis.",
        "content" : [
            {
                "type": "text",
                "text": "You are going to call the securities if something is suspicioun in the bag xray"
            },
            {
                "type": "",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{encoded_image}"
                }
            }
        ]
    }
]

template = """"
You receive information from a specialist that knows if someone is trying to sneak a weapon to an airport

The Specialist said: {context}

information: {information}
"""

llama_template = ChatPromptTemplate.from_template(template)
vision_template = ChatPromptTemplate.from_template(llama_vision_template)

llamaVisionModel = OllamaLLM(model = "llama3.2-vision")

llama_model = OllamaLLM(model = "llama3.1")

llama_chain = llama_template | llama_model
vision_chain = vision_template | llamaVisionModel

vision_result = vision_chain.invoke({
    "image": encoded_image
})

print("Main security guard: " + vision_result)

llama_result = llama_chain.invoke({
    "context": vision_result,
    "information": ""
})

print("Assistant: " + llama_result)