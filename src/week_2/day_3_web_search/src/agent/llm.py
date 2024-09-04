# import library
from langchain_groq import ChatGroq
from src.config.appconfig import groq_key



def LLM_Model():
    # Define the model names
    groq_model_name = [
        "mixtral-8x7b-32768",
        "llama3-8b-8192",
        "claude-3-opus-20240229",
    ]

    llm = ChatGroq(temperature=0,  # Set the temperature to 0
                   groq_api_key=groq_key,   # Set the API key
                   model_name=groq_model_name[1]  # Use the first model in the list
                   )
    
    # Return the initialized model
    return llm
