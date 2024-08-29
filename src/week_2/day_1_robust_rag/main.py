# import numpy as np
import os
from llama_index.llms.groq import Groq
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

print("...")

from dotenv import load_dotenv
load_dotenv()

# Set GROQ_API_KEY = "your api key" in the .env file, then load it below
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
# print(GROQ_API_KEY)

models = [
    # "llama-3.1-405b-reasoning",
    "llama-3.1-70b-versatile",
    "llama-3.1-8b-instant",
    "mixtral-8x7b-32768",
    "claude-3-5-sonnet",
    "gemini-1.5-flash",
    "gemini-1.5-pro",
]



"""
In llama-index, the LLM and embed_model can be set at any of 2 levels:
    - global seting with Settings (both llm and embed_model)
    - index level (embed_model only)
    - query engine level (llm only)
"""


Settings.embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5"
)

# Settings.llm = Groq(
#     models[0], 
#     api_key = GROQ_API_KEY,
#     temperature = 0.1
# )


def upload_doc(dir):

    print("Uploading...")
    documents = SimpleDirectoryReader(dir).load_data() 
    index = VectorStoreIndex.from_documents(documents)

    return index


def qa_engine(query: str, index, llm_client):
    
    query_engine = index.as_query_engine(llm=llm_client, similarity_top_k=5)
    response = query_engine.query(query)

    return response


if __name__ == "__main__":
    index = upload_doc("./data")
    query = input("Ask me anything: ")
    model = input("Enter model code: ")

    llm_client = Groq(model, api_key=GROQ_API_KEY, temperature=0.1)

    response = qa_engine(query, index, llm_client)

    print(response)

