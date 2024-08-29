# import libraries
import os
import argparse
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
load_dotenv('.env')

def get_response_from_chroma(query: str) -> str:
    # Load your OpenAI API Key
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')  # Add your OpenAI API Key
    CHROMA_PATH = "/usr/local/airflow/chromadb"  # ChromaDB Path
    #CHROMA_PATH = r"C:\Users\wave\Documents\llm\chromadb"

    # Initialize the OpenAI Embedding model
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

    # Connect to the existing ChromaDB
    db_chroma = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)

    # Retrieve context - top 5 most relevant (closest) chunks to the query vector
    docs_chroma = db_chroma.similarity_search_with_score(query, k=5)

    # Generate an answer based on given user query and retrieved context information
    context_text = "\n\n".join([doc.page_content for doc, _score in docs_chroma])

    # Use a prompt template
    PROMPT_TEMPLATE = """
    Answer the question based only on the following context:
    {context}
    Answer the question based on the above context: {question}.
    Provide a detailed answer.
    Don’t justify your answers.
    Don’t give information not mentioned in the CONTEXT INFORMATION.
    Do not say "according to the context" or "mentioned in the context" or similar.
    """

    # Load retrieved context and user query in the prompt template
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query)

    # Call LLM model to generate the answer based on the given context and query
    model = ChatOpenAI()
    response_text = model.predict(prompt)

    return response_text

if __name__ == "__main__":
    # Setup argument parser
    parser = argparse.ArgumentParser(description="Query ChromaDB and get a response.")
    parser.add_argument("query", type=str, help="The query to search in ChromaDB")

    # Parse the command-line arguments
    args = parser.parse_args()

    # Get the response from ChromaDB based on the query
    response = get_response_from_chroma(args.query)

    print("\n")
    print("Response: below")
    print("\n")
    # Print the response
    print(response)
